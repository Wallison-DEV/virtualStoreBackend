from rest_framework import serializers
from .models import ProductModel, CategoryModel, ProductLineModel

class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = ProductModel
        fields = ['name', 'description', 'price', 'stock', 'category']

    def validate_category(self, value):
        try:
            category = CategoryModel.objects.get(id=value)
        except (CategoryModel.DoesNotExist, ValueError):
            try:
                category = CategoryModel.objects.get(name=value)
            except CategoryModel.DoesNotExist:
                raise serializers.ValidationError("Category does not exist")
        
        return category

    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category'] = category if isinstance(category, CategoryModel) else category
        return super().create(validated_data)


class ProductLineSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ProductModel.objects.all())

    class Meta:
        model = ProductLineModel
        fields = ['product', 'quantity']