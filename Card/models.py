from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

class CardModel(models.Model):
    owner_name = models.CharField(max_length=255, verbose_name="Nome do Titular")
    cpf_owner = models.CharField(
        max_length=11, 
        validators=[RegexValidator(regex='^\d{11}$', message='CPF deve ter 11 dígitos')], 
        verbose_name="CPF do Titular"
    )
    name_in_card = models.CharField(max_length=255, verbose_name="Nome no Cartão")
    card_number = models.CharField(
        unique = True,
        max_length=16, 
        validators=[RegexValidator(regex=r'^\d{13,16}$', message='Número de cartão inválido')]
    )
    expires_month = models.IntegerField(
        verbose_name="Mês de Expiração",
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )  
    expires_year = models.IntegerField(validators=[MinValueValidator(2026)], verbose_name="Ano de Expiração") 
    cvv = models.CharField(max_length=4, verbose_name="CVV") 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='cards_list'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name_in_card} | ****{self.card_number[-4:]}'