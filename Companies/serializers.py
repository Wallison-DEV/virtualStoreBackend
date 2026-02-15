from rest_framework import serializers
from .models import CompanyModel, CompanyProductLine, Rating

class RatingSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    product_line = serializers.StringRelatedField()

    class Meta:
        model = Rating
        fields = ['id', 'user', 'product_line', 'value', 'comment', 'created_at']

class CompanyProductLineSerializer(serializers.ModelSerializer):
    product_line_ratings = serializers.SerializerMethodField()
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CompanyProductLine
        fields = ['id', 'product_name', 'quantity', 'product_line_ratings']
        
    def get_product_line_ratings(self, obj):
        ratings = obj.product_line_ratings.all().order_by('-created_at')
        return RatingSerializer(ratings, many=True).data
        
class CompanySerializer(serializers.ModelSerializer):
    product_lines = CompanyProductLineSerializer(many=True, read_only=True)
    orders_as_seller = serializers.SerializerMethodField()

    class Meta:
        model = CompanyModel
        fields = [
            'id', 'username', 'email', 'phone_number', 'address', 
            'registration_number', 'created_at', 
            'updated_at', 'product_lines', 'orders_as_seller'
        ]

    def get_orders_as_seller(self, obj):
        orders = obj.orders_as_seller.all()
        from Orders.serializers import OrderSerializer
        return OrderSerializer(orders, many=True).data
