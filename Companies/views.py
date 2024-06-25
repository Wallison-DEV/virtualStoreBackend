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

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

class CompanyProductLineViewSet(viewsets.ModelViewSet):
    queryset = CompanyProductLine.objects.all()
    serializer_class = CompanyProductLineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        filters = request.data.get('filters', {})
        category_query = filters.get('category', '')
        content_query = filters.get('content', '')
        order_query = filters.get('order_by', '')

        filtered_products = CompanyProductLine.objects.all()

        if category_query:
            filtered_products = filtered_products.filter(product__category=category_query)
        
        if content_query:
            filtered_products = filtered_products.filter(product__name__icontains=content_query)
        
        if order_query:
            filtered_products = filtered_products.order_by(order_query)

        page = self.paginate_queryset(filtered_products)
        if page is not None:
            serializer = self.get_paginated_response(self.get_serializer(page, many=True).data)
        else:
            serializer = self.get_serializer(filtered_products, many=True)

        return Response(serializer.data)
