from rest_framework import serializers
from .models import UserModel
from Address.models import AddressModel
from Card.models import CardModel
from Orders.models import OrderModel

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True, source='orders_as_buyer')

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'date_of_birth', 'addresses', 'cards', 'orders']

class AddAddressSerializer(serializers.Serializer):
    address_id = serializers.PrimaryKeyRelatedField(queryset=AddressModel.objects.all())

class AddCardSerializer(serializers.Serializer):
    card_id = serializers.PrimaryKeyRelatedField(queryset=CardModel.objects.all())