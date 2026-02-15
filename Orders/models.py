from django.db import models
from django.forms import ValidationError
from Address.models import AddressModel
from UsersAccounts.models import UserModel 
from Companies.models import CompanyModel
from Products.models import ProductModel
from Card.models import CardModel

class OrderModel(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('PIX', 'PIX'),
        ('boleto', 'Boleto'),
        ('cartao', 'Cartão'),
    ]
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    buyer = models.ForeignKey(UserModel, related_name='orders_as_buyer', on_delete=models.DO_NOTHING, verbose_name='Comprador')
    seller = models.ForeignKey(CompanyModel, related_name='orders_as_seller', on_delete=models.DO_NOTHING, verbose_name='Vendedor')
    order_address = models.ForeignKey(AddressModel, on_delete=models.DO_NOTHING, verbose_name='Endereço de entrega')
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor total do pedido', default=0.0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Status do pedido')
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Método de pagamento')
    installments = models.IntegerField(verbose_name='Parcelas', default=1)
    card_pay = models.ForeignKey(CardModel, on_delete=models.DO_NOTHING, verbose_name='Cartão de pagamento', null=True, blank=True)
    pix_code = models.CharField(max_length=255, verbose_name='Código PIX para pagamento', null=True, blank=True)
    bar_code = models.CharField(max_length=255, verbose_name='Código de barras do boleto para pagamento', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    def __str__(self):
        return f'Pedido #{self.id} - {self.buyer}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def update_total(self):
        total = sum(item.quantity * item.price_at_purchase for item in self.items.all())
        self.total_amount = total
        super(OrderModel, self).save(update_fields=['total_amount'])
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.status = 'pending'

        if self.payment_method == 'PIX' and not self.pix_code:
            self.pix_code = "PIX-GERADO-AUTOMATICO-123456"
            self.bar_code = None
            self.card_pay = None
            self.installments = 1
        
        elif self.payment_method == 'boleto' and not self.bar_code:
            self.bar_code = "23793.38128 60087.003457 05000.643048 1 9000000010000"
            self.pix_code = None
            self.card_pay = None
            self.installments = 1

        elif self.payment_method == 'cartao':
            self.pix_code = None
            self.bar_code = None

        super().save(*args, **kwargs)


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2) 

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.price_at_purchase = self.product.base_price

            from Companies.models import CompanyProductLine
            stock = CompanyProductLine.objects.filter(
                company=self.order.seller, 
                product=self.product
            ).first()

            if not stock or stock.quantity < self.quantity:
                raise ValidationError(f"Estoque insuficiente para {self.product.name}")
            
            stock.quantity -= self.quantity
            stock.save()

        super().save(*args, **kwargs)
        
        self.order.update_total()
