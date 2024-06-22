from rest_framework import serializers
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'price', 'current_price', 'discount', 'last_price', 'category']

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
