from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import ProductModel
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug' 
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category'] 
    search_fields = ['name', 'description']
    ordering_fields = ['base_price', 'created_at']
