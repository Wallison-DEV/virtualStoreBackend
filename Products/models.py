from django.db import models
from django.utils.text import slugify

class Category(models.TextChoices):
    ELECTRONICS = 'EL', 'Electronics & Technology'
    FASHION = 'FA', 'Fashion & Accessories'
    HOME_KITCHEN = 'HK', 'Home & Kitchen'
    BEAUTY_CARE = 'BC', 'Beauty & Personal Care'
    SPORTS_OUTDOORS = 'SO', 'Sports & Outdoors'
    BABY_KIDS = 'BK', 'Baby & Kids'
    HEALTH_WELLNESS = 'HW', 'Health & Wellness'
    BOOKS_MEDIA = 'BM', 'Books & Media'
    FOOD_BEVERAGES = 'FB', 'Food & Beverages'
    AUTOMOTIVE_TOOLS = 'AT', 'Automotive & Tools'
    PET_SHOP = 'PS', 'Pet Shop'
    OUTDOORS_GARDENING = 'OG', 'Outdoors & Gardening'

class ProductModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome do produto")

    slug = models.SlugField(unique=True, blank=True, null=True) 
    sku = models.CharField(max_length=50, unique=True, default="TEMP-SKU", verbose_name="SKU/Código")

    description = models.TextField(verbose_name="Descrição do produto", blank=True, null=True)
    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.ELECTRONICS,
        verbose_name="Categoria"
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Base", default=0.0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Desconto", default=0)

    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagem do Produto")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    @property
    def current_price(self):
        if self.discount_percentage > 0:
            return self.base_price * (1 - (self.discount_percentage / 100))
        return self.base_price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sku} - {self.name}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']
