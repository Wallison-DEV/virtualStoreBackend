from rest_framework import serializers
from .models import CardModel

class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardModel
        fields = '__all__'