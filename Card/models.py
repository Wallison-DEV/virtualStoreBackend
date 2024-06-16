from django.core.validators import RegexValidator
from django.db import models

class CardModel(models.Model):
    owner_name = models.CharField(max_length=255, null=False, blank=False)
    cpf_owner = models.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$', message='CPF deve ter 11 dígitos')], null=False, blank=False)
    name_in_card = models.CharField(max_length=255, null=False, blank=False)
    card_number = models.CharField(max_length=16, null=False, blank=False)  
    expires_month = models.CharField(max_length=2, null=False, blank=False)  
    expires_year = models.CharField(max_length=4, null=False, blank=False) 
    cvv = models.CharField(max_length=4, null=False, blank=False) 
    user_id = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.owner_name}, {self.name_in_card}, {self.card_number}'
