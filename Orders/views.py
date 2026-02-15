from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import OrderModel, OrderItemModel
from .serializers import OrderSerializer, OrderItemSerializer
from Companies.models import CompanyModel

class ProductLineViewSet(viewsets.ModelViewSet):
    queryset = OrderItemModel.objects.all()
    serializer_class = OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'registration_number'): # É empresa
            return OrderModel.objects.filter(seller__user=user)
        return OrderModel.objects.filter(buyer=user)

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)
