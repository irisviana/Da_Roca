from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField

from products.models import Product
from users.models import User, Address

# Create your models here.
class CartProduct(models.Model):
    quantity = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)

class Payment(models.Model):
    PAYMENT_TYPE = (
        ('C', 'Dinheiro'),
        ('CC', 'Cartão de crédito'),
        ('DC', 'Cartão de débito'),
    )

    PAYMENT_STATUS = (
        (0, 'Pendente'),
        (1, 'Pago'),
    )

    type = models.CharField(max_length=2, null=False, blank=False)
    change = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2)
    status = models.IntegerField(null=False, blank=False, choices=PAYMENT_STATUS)
class Order(models.Model):
    ORDER_STATUS = (
        (0, 'Espera'),
        (1, 'Preparação'),
        (2, 'Entrega'),
        (3, 'Concluído'),
        (4, 'Cancelado')
    )
    status = models.IntegerField(null=False, blank=False, choices=ORDER_STATUS)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(null=False, blank=False, max_digits=19, decimal_places=2)

class OrderProduct(models.Model):
    quantity = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(
       Product, on_delete=models.CASCADE, null=False, blank=False)
    order = models.ForeignKey(
        Order, on_delete=CASCADE, null=False, blank=False)