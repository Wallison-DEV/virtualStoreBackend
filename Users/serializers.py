from rest_framework import serializers
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id", 
            "username", 
            "email", 
            "first_name", 
            "last_name", 
            "date_of_birth", 
            "phone_number", 
            "is_staff", 
            "is_active", 
            "date_joined", 
            "last_login"
        )
