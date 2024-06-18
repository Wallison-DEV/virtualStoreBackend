from django.db import models
from Products.models import ProductLineModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from UsersAccounts.models import UserModel

class CompanyModel(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    email = models.EmailField(max_length=255, verbose_name="Email da Empresa", unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="Número de Telefone", null=True, blank=True)
    address = models.TextField(verbose_name="Endereço da Empresa")
    registration_number = models.CharField(max_length=50, verbose_name="Número de Registro", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    products = models.ManyToManyField(ProductLineModel, verbose_name='Lista de produtos', related_name='companies')
    average_rating = models.FloatField(verbose_name="Classificação Média", default=0)

    def update_average_rating(self):
        ratings = self.ratings.all()
        self.average_rating = sum(rating.value for rating in ratings) / ratings.count() if ratings.exists() else 0
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class Rating(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ['company', 'user']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.company.update_average_rating()

    def delete(self, *args, **kwargs):
        company = self.company
        super().delete(*args, **kwargs)
        company.update_average_rating()
