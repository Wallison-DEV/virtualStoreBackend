from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.db import models

class AddressModel(models.Model):
    address = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    state = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    zip = models.CharField(max_length=20, validators=[MinLengthValidator(3)], null=False, blank=False)
    city = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    receiver_name = models.CharField(max_length=200, validators=[MinLengthValidator(3)], null=False, blank=False)
    receiver_cpf = models.CharField(max_length=11, validators=[RegexValidator(regex='^\d{11}$', message='CPF deve ter 11 dígitos')], null=False, blank=False)
    user_id = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.country}'
