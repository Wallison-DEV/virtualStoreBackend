from rest_framework import viewsets

from .models import OrderModel
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer