from rest_framework import serializers
from Orders.serializers import OrderSerializer 

from .models import CompanyModel, CompanyProductLine, Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product_line', 'value', 'comment', 'created_at']

class CompanyProductLineSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    product = serializers.StringRelatedField()

    class Meta:
        model = CompanyProductLine
        fields = ['id', 'product', 'quantity', 'ratings']
        
    def get_rating(self, obj):
        rating_data = Rating.objects.filter(product_line=obj)
        rating_serializer = RatingSerializer(rating_data, many=True)
        return rating_serializer.data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = self.get_rating(instance).order_by('created_at')
        
        return representation
        
class CompanySerializer(serializers.ModelSerializer):
    products = CompanyProductLineSerializer(many=True, read_only=True)
    orders_as_seller = serializers.SerializerMethodField()

    class Meta:
        model = CompanyModel
        fields = [
            'id', 'username', 'email', 'phone_number', 'address', 'password', 'registration_number',
            'created_at', 'updated_at', 'products', 'orders_as_seller'
        ]

    def get_orders_as_seller(self, obj):
        orders = obj.orders_as_seller.all()
        return OrderSerializer(orders, many=True).data
    
    def get_products(self, obj):
        menu_data = CompanyProductLine.objects.filter(company=obj)
        menu_serializer = CompanyProductLineSerializer(menu_data, many=True)
        return menu_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = self.get_products(instance)
        return representation
