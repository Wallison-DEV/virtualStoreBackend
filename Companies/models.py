from django.db import models
from Products.models import ProductModel, ProductLineModel

class CompanyModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome da Empresa")
    email = models.EmailField(max_length=255, verbose_name="Email da Empresa", unique=True)
    phone_number = models.CharField(max_length=15, verbose_name="Número de Telefone", null=True, blank=True)
    address = models.TextField(verbose_name="Endereço da Empresa")
    registration_number = models.CharField(max_length=50, verbose_name="Número de Registro", unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    menu = models.ForeignKey(ProductLineModel, on_delete=models.DO_NOTHING, verbose_name='Lista de produtos')
    rating = models.IntegerField(verbose_name="Classificação", choices=[
        (1, '1 estrela'),
        (2, '2 estrelas'),
        (3, '3 estrelas'),
        (4, '4 estrelas'),
        (5, '5 estrelas'),
    ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"