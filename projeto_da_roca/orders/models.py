from django.db import models

from products.models import Product
from users.models import User, Address


# Create your models here.


class CartProduct(models.Model):
    quantity = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)


# Coloca isso dentro do models de pedido
# METHOD_CHOICES = (
#         ("cash", 'Outros'),
#         ("credit_card", 'Cartão de Crédito'),
#         ("debit_card", 'Cartão de debito'),
#     )
# payment_method = models.CharField(max_length=25, choices=METHOD_CHOICES, null=True, blank=True)
#
# delivery_address = models.ForeignKey(
#     Address, on_delete=models.SET_NULL, null=True, blank=True)
