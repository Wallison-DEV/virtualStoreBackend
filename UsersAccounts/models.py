from django.db import models
from django.contrib.auth.models import AbstractUser
from Address.models import AddressModel
from Card.models import CardModel

class UserModel(AbstractUser):
    date_of_birth = models.DateField(verbose_name="Data de nascimento", null=True, blank=True)
    address = models.ForeignKey(AddressModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Endereço")
    cards = models.ManyToManyField(CardModel, blank=True, verbose_name="Cartões")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_model_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_model_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
