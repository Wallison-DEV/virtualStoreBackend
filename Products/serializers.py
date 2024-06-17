from rest_framework import serializers
from .models import ProductModel, CategoryModel, ProductLineModel

class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'
        
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'
        
class ProductLineSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.all())

    class Meta:
        model = ProductLineModel
        fields = ['product', 'quantity']