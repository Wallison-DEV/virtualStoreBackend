from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import OrderModel
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        buyer = request.user
        seller_id = request.data.get('seller_id')
        seller = CompanyModel.objects.get(id=seller_id)

        order_data = serializer.validated_data
        items_data = order_data.pop('items')

        order = OrderModel.objects.create(buyer=buyer, seller=seller, **order_data)

        for item_data in items_data:
            product_id = item_data['product']
            quantity = item_data['quantity']
            product = ProductModel.objects.get(id=product_id)
            ProductLineModel.objects.create(product=product, quantity=quantity)

        headers = self.get_success_headers(serializer.data)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)
