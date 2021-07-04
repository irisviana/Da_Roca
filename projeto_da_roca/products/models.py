from django.db import models
from django.shortcuts import get_object_or_404
from users.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    def __str__(self):
        return u'{0}'.format(self.name)


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
    product_pic = models.ImageField(upload_to='static/productImages/', default='static/productImages/img_default.png')

    def __str__(self):
        return '{} | {} - {}'.format(self.id, self.name, self.variety)


    def searchSellerName(self):
        seller = get_object_or_404(User, id=self.user.id)
        name = seller.first_name + ' ' + seller.last_name
        return name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
