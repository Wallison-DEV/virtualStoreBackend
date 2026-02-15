from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.filters import OrderingFilter
from .models import CompanyModel, CompanyProductLine, Rating
from Products.models import ProductModel
from .serializers import CompanySerializer, CompanyProductLineSerializer, RatingSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CompanyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CompanyModel.objects.prefetch_related(
        'product_lines__product', 
        'product_lines__product_line_ratings'
    )

    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class CompanyProductLineViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyProductLineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['quantity', 'product__name']

    def get_queryset(self):
        params = self.request.query_params
        category = params.get('category')
        content = params.get('content')

        queryset = CompanyProductLine.objects.select_related('product').all()
    
        if category:
            queryset = queryset.filter(product__category=category)
        
        if content:
            queryset = queryset.filter(product__name__icontains=content)

        return queryset