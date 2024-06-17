from rest_framework import viewsets

from .models import ProductModel
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel
    serializer_class = ProductSerializer