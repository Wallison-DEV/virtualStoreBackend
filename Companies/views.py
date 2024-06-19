from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import CompanyModel, Rating
from .serializers import CompanySerializer, RatingSerializer
from Products.models import ProductLineModel
from Products.serializers import ProductLineSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        company = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = ProductModel.objects.get(id=product_id)
            product_line, created = ProductLineModel.objects.get_or_create(product=product, defaults={'quantity': quantity})
            if not created:
                product_line.quantity = quantity
                product_line.save()
                
            if request.user != company:
                return Response({'error': 'You are not authorized to add products to this company'}, status=status.HTTP_403_FORBIDDEN)
            
            company.menu.add(product_line)
            return Response({'status': 'product added or updated'}, status=status.HTTP_200_OK)
        except ProductModel.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_rating(self, request, pk=None):
        company = self.get_object()
        user = request.user
        value = request.data.get('value')

        if value is None or not (1 <= int(value) <= 5):
            return Response({'error': 'Rating value must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            company=company,
            user=user,
            defaults={'value': value}
        )

        return Response(RatingSerializer(rating).data)
    
    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        company = self.get_object()
        product_line_id = request.data.get('product_line_id')

        try:
            product_line = company.menu.get(id=product_line_id)
        except ProductLineModel.DoesNotExist:
            return Response({'error': 'Product not found in company menu'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user != company:
            return Response({'error': 'You are not authorized to delete this product'}, status=status.HTTP_403_FORBIDDEN)

        product_line.delete()
        return Response({'status': 'product deleted'}, status=status.HTTP_204_NO_CONTENT)
