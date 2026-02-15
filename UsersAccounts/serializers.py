from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'password', 'cards', 'address']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(serializers.Serializer):
    username_or_email_or_registration = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username_or_email_or_registration')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Credenciais inválidas ou conta inativa.')

        return self.generate_tokens(user)

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        
        from Companies.models import CompanyModel
        is_company = isinstance(user, CompanyModel)
        refresh['is_company'] = is_company 

        if is_company:
            from Companies.serializers import CompanySerializer
            data = CompanySerializer(user).data
        else:
            from .serializers import UserSerializer
            data = UserSerializer(user).data

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': data,
            'is_company': is_company
        }
