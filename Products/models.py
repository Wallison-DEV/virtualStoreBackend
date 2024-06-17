from django.db import models

class CategoryModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome da categoria")
    description = models.TextField(verbose_name="Descrição da categoria", blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

class ProductModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do produto")
    description = models.TextField(verbose_name="Descrição do produto", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, verbose_name="Categoria")
    stock = models.PositiveIntegerField(verbose_name="Estoque", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']
