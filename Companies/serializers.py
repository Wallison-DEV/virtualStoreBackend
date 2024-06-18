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
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    orders_as_seller = OrderSerializer(many=True, read_only=True) 

    class Meta:
        model = CompanyModel
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'registration_number', 'created_at', 'updated_at', 'products', 'average_rating', 'ratings', 'orders_as_seller']
