from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserModel
from .serializers import UserSerializer, AddAddressSerializer, AddCardSerializer
from Address.models import AddressModel
from Card.models import CardModel

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        user = self.get_object()
        serializer = AddAddressSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data['address_id']
            try:
                user.add_address(address)
                return Response({'status': 'address added'})
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_address(self, request, pk=None):
        user = self.get_object()
        address_id = request.data.get('address_id')
        try:
            address = AddressModel.objects.get(id=address_id)
            user.remove_address(address)
            return Response({'status': 'address removed'})
        except AddressModel.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_card(self, request, pk=None):
        user = self.get_object()
        serializer = AddCardSerializer(data=request.data)
        if serializer.is_valid():
            card = serializer.validated_data['card_id']
            try:
                user.add_card(card)
                return Response({'status': 'card added'})
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_card(self, request, pk=None):
        user = self.get_object()
        card_id = request.data.get('card_id')
        try:
            card = CardModel.objects.get(id=card_id)
            user.remove_card(card)
            return Response({'status': 'card removed'})
        except CardModel.DoesNotExist:
            return Response({'error': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)
