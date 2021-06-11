from django.db import models
from users.models import User


# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    variety = models.CharField(max_length=200, null=True, blank=True)
    expiration_days = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    stock_amount = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, blank=False)
