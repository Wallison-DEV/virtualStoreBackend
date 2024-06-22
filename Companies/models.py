from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from UsersAccounts.models import UserModel
from Products.models import ProductModel

class CompanyModel(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    email = models.EmailField(max_length=255, verbose_name="Email da Empresa", unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="Número de Telefone", null=True, blank=True)
    address = models.TextField(verbose_name="Endereço da Empresa")
    registration_number = models.CharField(max_length=50, verbose_name="Número de Registro", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class CompanyProductLine(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE, related_name='product_lines', verbose_name='Empresa')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name='Produto')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    class Meta:
        verbose_name = 'Linha de Produto da Empresa'
        verbose_name_plural = 'Linhas de Produtos das Empresas'
        unique_together = ('company', 'product')

class Rating(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='ratings')
    product_line = models.ForeignKey(CompanyProductLine, on_delete=models.CASCADE, related_name='product_line_ratings')
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Nota')
    comment = models.TextField(verbose_name='Comentário', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')

    def __str__(self):
        return f'Rating {self.value} by {self.user.username} for {self.product_line.product.name}'

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        unique_together = ('user', 'product_line')
