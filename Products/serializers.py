from rest_framework import serializers
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'price', 'current_price', 'discount', 'last_price', 'category']
        read_only_fields = ['current_price', 'discount', 'last_price']