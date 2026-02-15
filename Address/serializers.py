from rest_framework import serializers
from .models import AddressModel

class AddressSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AddressModel
        fields = '__all__'
        read_only_fields = ['user']