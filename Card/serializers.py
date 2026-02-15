from rest_framework import serializers
from datetime import datetime
from .models import CardModel

class CardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = CardModel
        fields = ['username','owner_name', 'cpf_owner', 'name_in_card', 'card_number', 'expires_month', 'expires_year', 'cvv']
        read_only_fields = ['user','created_at','updated_at']

    def validade_cpf_owner(self, value):
        cleaned_values = ''.join(filter(str.isdigit, value))

        if len(cleaned_values) != 11:
            raise serializers.ValidationError("O CPF deve conter exatamente 11 números.")
            
        return cleaned_values
    
    def validate(self, data):
        month = int(data.get('expires_month'))
        year = int(data.get('expires_year'))

        if year < 100: year += 2000

        now = datetime.now()
        if year < now.year or (year == now.year and month < now.month):
            raise serializers.ValidationError("O cartão já está expirado.")

        if month < 1 or month > 12:
            raise serializers.ValidationError("Mês de expiração inválido, deve ser entre 1 e 12.")
        
        return data

    def to_representation(delf, instance):
        representation = super().to_representation(instance)

        num = representation['card_number']
        representation['card number'] = f"**** **** **** {num[-4:]}"
        
        return representation