from rest_framework import serializers
from .models import AddressModel

class AddressModelSerializer(serializers.ModelSerializer):
    class Meta: 
        model = AddressModel
        fields = '__all__'