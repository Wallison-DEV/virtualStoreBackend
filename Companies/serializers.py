from rest_framework import serializers
from .models import CompanyModel, Rating
from Orders.serializers import OrderSerializer 
from Products.serializers import ProductLineSerializer

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['value']

class CompanySerializer(serializers.ModelSerializer):
    products = ProductLineSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True, source='ratings')
    average_rating = serializers.ReadOnlyField()
    orders_as_seller = serializers.SerializerMethodField()

    class Meta:
        model = CompanyModel
        fields = [
            'id', 'name', 'email', 'phone_number', 'address', 'registration_number',
            'created_at', 'updated_at', 'products', 'average_rating', 'ratings', 'orders_as_seller'
        ]

    def get_orders_as_seller(self, obj):
        orders = obj.orders_as_seller.all()
        return OrderSerializer(orders, many=True).data
