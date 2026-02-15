from rest_framework import serializers
from .models import OrderModel, OrderItemModel
from Companies.models import CompanyProductLine
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')

    class Meta:
        model = OrderItemModel
        fields = ['product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'buyer', 'seller', 'order_address', 'payment_method',
                  'status', 'installments', 'card_pay', 'pix_code', 'bar_code', 
                  'items', 'total_amount']
        read_only_fields = ['buyer', 'pix_code', 'bar_code', 'status', 'total_amount']

    def validate(self, data):
        payment_method = data.get('payment_method')
        
        if payment_method != 'cartao':
            data['installments'] = 1  
            data['card_pay'] = None  
        else:
            if not data.get('card_pay'):
                raise serializers.ValidationError({"card_pay": "Cartão obrigatório para este método."})
            if data.get('installments', 1) < 1:
                 raise serializers.ValidationError({"installments": "Mínimo de 1 parcela."})

        if payment_method == 'PIX':
            data['pix_code'] = "PIX-RANDOM-CODE-123456789"
            data['bar_code'] = None
        elif payment_method == 'boleto':
            data['bar_code'] = "23793.38128 60087.003457 05000.643048 1 9000000010000"
            data['pix_code'] = None
        else:
            data['pix_code'] = None
            data['bar_code'] = None

        return data

    @transaction.atomic
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderModel.objects.create(**validated_data)

        for item_data in items_data:
            OrderItemModel.objects.create(
                order=order,
                product_id=item_data['product']['id'],
                quantity=item_data['quantity']
            )
        
        order.refresh_from_db() 
        return order

    def update(self, instance, validated_data):
        user = self.context['request'].user
        new_status = validated_data.get('status')

        if user == instance.buyer:
            if new_status == 'canceled' and instance.status == 'pending':
                return self._change_status(instance, 'canceled', refund_stock=True)
            raise serializers.ValidationError(f'Compradores só podem cancelar pedidos pendentes.')

        if user == instance.seller.user:
            if instance.status == 'delivered':
                raise serializers.ValidationError(f'Pedidos entregues não podem ser alterados')
            return self._change_status(instance, new_status, refund_stock=True)
        
        return instance
    
    def _change_status(self, instance, status, refund_stock=False):
        if refund_stock:
            for item in instance.items.all():
                stock_item = CompanyProductLine.objects.get(company=instance.seller, product=instance.product)
                stock_item.quantity += item.quantity
                stock_item.save()
        instance.status = status
        instance.save()
        return instance

