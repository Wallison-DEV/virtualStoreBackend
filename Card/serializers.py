from rest_framework import serializers
from .models import CardModel

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = '__all__'