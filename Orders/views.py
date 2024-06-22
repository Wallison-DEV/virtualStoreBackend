from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import OrderModel, ProductLineModel
from .serializers import OrderSerializer, ProductLineSerializer
from Companies.models import CompanyModel

class ProductLineViewSet(viewsets.ModelViewSet):
    queryset = ProductLineModel.objects.all()
    serializer_class = ProductLineSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        buyer = request.user
        seller_id = serializer.validated_data.get('seller_id')
        seller = CompanyModel.objects.get(id=seller_id)

        if buyer != request.user:
            return Response({'error': 'You are not authorized to create this order for another user'}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = serializer.save()
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            updated_instance = serializer.save()
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(OrderSerializer(updated_instance).data)
