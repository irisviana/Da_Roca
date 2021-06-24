from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class CartProduct(models.Model):
    quantity = models.IntegerField(null=False, blank=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)