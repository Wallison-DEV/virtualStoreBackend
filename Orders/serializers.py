from rest_framework import serializers
from .models import OrderModel
from Products.serializers import ProductLineSerializer
from Products.models import ProductLineModel, ProductModel
from Card.models import CardModel
from Companies.models import CompanyModel

class OrderSerializer(serializers.ModelSerializer):
    items = ProductLineSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'buyer', 'seller', 'order_address', 'payment_method', 'status', 'installments', 'card_pay', 'pix_code', 'bar_code', 'items']
        read_only_fields = ['seller']

    def validate(self, data):
        payment_method = data.get('payment_method')

        if payment_method == 'PIX':
            data['pix_code'] = "12345678901234567890"
        elif payment_method == 'boleto':
            data['bar_code'] = "12345678901234567890123456789012345678901234"

        return data

    def update(self, instance, validated_data):
        user = self.context['request'].user
        status = validated_data.get('status')

        if user == instance.buyer:
            if instance.status in ['delivered', 'declined', 'shipped']:
                raise serializers.ValidationError({"status": "Você não pode alterar o status de um pedido entregue, recusado ou enviado."})
            
            if status in ['pending', 'canceled']:
                instance.status = status
                instance.save()
                return instance

        elif user == instance.seller:
            if instance.status == 'delivered':
                raise serializers.ValidationError({"status": "Você não pode alterar o status de um pedido entregue."})
            
            if status in ['pending', 'shipped', 'canceled']:
                instance.status = status
                instance.save()
                return instance

        raise serializers.ValidationError({"status": "Você não tem permissão para alterar o status do pedido para o estado desejado."})

        return instance

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderModel.objects.create(**validated_data)
        for item_data in items_data:
            ProductLineModel.objects.create(order=order, **item_data)
        return order
