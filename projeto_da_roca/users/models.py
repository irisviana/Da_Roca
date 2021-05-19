from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('customer', 'Cliente'),
        ('producer', 'Produtor'),
    )
    user_type = models.CharField(max_length=10, default='customer', choices=USER_TYPE_CHOICES)
    cpf = models.CharField(max_length=11, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('user', 'Usuário'),
        ('order', 'Pedido'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    address_type = models.CharField(max_length=5, default='user', choices=ADDRESS_TYPE_CHOICES)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    house_number = models.CharField(max_length=10, null=True, blank=True)
