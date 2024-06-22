from rest_framework import serializers
from .models import OrderModel, ProductLineModel
from Products.models import ProductModel
from Companies.models import CompanyModel
from rest_framework import status

class ProductLineSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.all())

    class Meta:
        model = ProductLineModel
        fields = ['product', 'quantity']

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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderModel.objects.create(**validated_data)

        for item_data in items_data:
            self.create_product_line(order, item_data)

        return order

    def update(self, instance, validated_data):
        user = self.context['request'].user
        status = validated_data.get('status')

        if user == instance.buyer:
            if instance.status in ['delivered', 'declined', 'shipped']:
                raise serializers.ValidationError({"status": "You cannot change the status of an already delivered, declined, or shipped order."})
            
            if status in ['pending', 'canceled']:
                instance.status = status
                instance.save()
                self.update_stock(instance, increase=(status == 'canceled'))
                return instance

        elif user == instance.seller:
            if instance.status == 'delivered':
                raise serializers.ValidationError({"status": "You cannot change the status of an already delivered order."})
            
            if status in ['pending', 'shipped', 'canceled']:
                instance.status = status
                instance.save()
                self.update_stock(instance, increase=(status == 'canceled'))
                return instance

        raise serializers.ValidationError({"status": "You do not have permission to change the order status to the desired state."})

    def create_product_line(self, order, item_data):
        product_id = item_data['product']
        quantity = item_data['quantity']
        product = ProductModel.objects.get(id=product_id)
        seller = order.seller

        if not seller.products.filter(product=product).exists():
            raise serializers.ValidationError({'error': f'Product {product.name} does not belong to seller {seller.name}'})
        
        product_line = seller.products.get(product=product)

        if quantity > product_line.quantity:
            raise serializers.ValidationError({'error': f'Insufficient stock of {product.name} at seller {seller.name}'})

        ProductLineModel.objects.create(order=order, product=product, quantity=quantity)

    def update_stock(self, order, increase=False):
        for item in order.items.all():
            if increase:
                item.product_line.quantity += item.quantity
            else:
                item.product_line.quantity -= item.quantity
            item.product_line.save()
