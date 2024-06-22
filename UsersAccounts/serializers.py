from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import UserModel
from Address.models import AddressModel
from Address.serializers import AddressSerializer
from Card.models import CardModel
from Card.serializers import CardSerializer
from Orders.models import OrderModel
from Orders.serializers import OrderSerializer
from Companies.models import CompanyModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        cards_qs = CardModel.objects.filter(user_id=instance.id)
        cards_serializer = CardSerializer(cards_qs, many=True)
        data['cards'] = cards_serializer.data
        
        address_qs = AddressModel.objects.filter(user_id=instance.id)
        address_serializer = AddressSerializer(address_qs, many=True)
        data['address'] = address_serializer.data
        
        orders_qs = OrderModel.objects.filter(buyer=instance)
        order_serializer = OrderSerializer(orders_qs, many=True)
        data['orders'] = order_serializer.data
        
        return data

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_or_email_or_registration = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email_or_registration = attrs.get('username_or_email_or_registration')  
        password = attrs.get('password')

        user = authenticate(email=username_or_email_or_registration, password=password)
        if user is None:
            user = authenticate(username=username_or_email_or_registration, password=password)
        if user is None:
            try:
                company = CompanyModel.objects.get(registration_number=username_or_email_or_registration)
                user = authenticate(username=company.username, password=password)
            except CompanyModel.DoesNotExist:
                user = None

        if user is None:
            raise serializers.ValidationError('No active account found with the given credentials')

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        user_serializer = UserSerializer(user)
        user_data = user_serializer.data

        return {
            'refresh': str(refresh),
            'access': str(access_token),
            'exp': access_token['exp'],
            'user': user_data,
        }
