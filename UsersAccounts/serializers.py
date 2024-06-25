from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from datetime import timedelta

from .models import UserModel
from Address.serializers import AddressSerializer
from Card.serializers import CardSerializer
from Orders.serializers import OrderSerializer
from Companies.models import CompanyModel
from Companies.serializers import CompanySerializer

class UserSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    address = AddressSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'date_of_birth', 'password', 'cards', 'address', 'orders']
        extra_kwargs = {'password': {'write_only': True}}

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_or_email_or_registration = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email_or_registration = attrs.get('username_or_email_or_registration')
        password = attrs.get('password')

        user = self.authenticate_credentials(username_or_email_or_registration, password)

        if not user:
            raise serializers.ValidationError('No active account found with the given credentials')

        return self.get_tokens_for_user(user)

    def authenticate_credentials(self, username_or_email_or_registration, password):
        user = authenticate(username=username_or_email_or_registration, password=password)
        if user:
            return user

        try:
            user = UserModel.objects.get(email=username_or_email_or_registration)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            company = CompanyModel.objects.get(registration_number=username_or_email_or_registration)
            if company.password == password:
                return company
            else:
                pass
        except CompanyModel.DoesNotExist:
            pass

        return None

    def get_tokens_for_user(self, user):
        if isinstance(user, UserModel):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_serializer = UserSerializer(user)
            user_data = user_serializer.data

            return {
                'refresh': str(refresh),
                'access': access_token,
                'exp': refresh.payload['exp'],
                'user': user_data,
            }
        elif isinstance(user, CompanyModel):
            return self.generate_refresh_token_for_company(user)
        else:
            raise serializers.ValidationError('Unexpected user type encountered during serialization')

    def generate_refresh_token_for_company(self, company):

        refresh = RefreshToken()
        refresh['user_id'] = company.pk
        refresh['username'] = company.username
        refresh['email'] = company.email
        refresh['registration_number'] = company.registration_number
        refresh.set_exp(lifetime=timedelta(hours=1))  

        access_token = str(refresh.access_token)
        exp = refresh.payload['exp']

        company_serializer = CompanySerializer(company)
        user_data = company_serializer.data

        return {
            'refresh': str(refresh),
            'access': access_token,
            'exp': exp,
            'user': user_data,
        }
