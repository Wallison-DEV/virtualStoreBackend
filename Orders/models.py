from django.db import models
from Address.models import AddressModel
from Users.models import UserModel 
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

    products = models.ForeignKey('OrderItem', related_name='items', on_delete=models.DO_NOTHING, verbose_name='Produtos')
    buyer = models.ForeignKey(UserModel, related_name='orders_as_buyer', on_delete=models.DO_NOTHING, verbose_name='Comprador')
    seller = models.ForeignKey(UserModel, related_name='orders_as_seller', on_delete=models.DO_NOTHING, verbose_name='Vendedor')
    order_address = models.ForeignKey(AddressModel, on_delete=models.DO_NOTHING, verbose_name='Endereço de entrega')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Método de pagamento')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Status do pedido')
    installments = models.IntegerField(verbose_name='Parcelas', default=1)
    card_pay = models.ForeignKey(CardModel, on_delete=models.DO_NOTHING, verbose_name='Cartão de pagamento', null=True, blank=True)
    pix_code = models.CharField(max_length=255, verbose_name='Código PIX para pagamento', null=True, blank=True)
    bar_code = models.CharField(max_length=255, verbose_name='Código de barras do boleto para pagamento', null=True, blank=True)
    
    def __str__(self):
        return f'Pedido #{self.id} - {self.buyer}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class OrderItem(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name='Produto')
    quantity = models.PositiveIntegerField(verbose_name='Quantidade')

    def __str__(self):
        return f'{self.product} x{self.quantity}'

    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Itens de Pedido'
