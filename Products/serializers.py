from rest_framework import serializers
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    current_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductModel
        fields = [
            'id', 'name', 'slug', 'description', 
            'base_price', 'current_price', 'discount_percentage', 'category'
        ]
        read_only_fields = ['slug', 'current_price']
