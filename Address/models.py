from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models
from django.conf import settings

class AddressModel(models.Model):
    zip = models.CharField(max_length=20, validators=[MinLengthValidator(3)], null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    state = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    city = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    receiver_name = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    receiver_cpf = models.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$', message='CPF deve ter 11 dígitos')], null=False, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.country}'
