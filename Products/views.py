from rest_framework import viewsets

from .models import ProductModel, CategoryModel, ProductLineModel
from .serializers import ProductSerializer, CategorySerializer, ProductLineSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    
class ProductLineViewSet(viewsets.ModelViewSet):
    queryset = ProductLineModel.objects.all()
    serializer_class = ProductLineSerializer
    