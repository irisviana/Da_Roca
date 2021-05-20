from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
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

class Profile(models.Model):
    PROFILE_TYPE_CHOICES = (
        ('admin', 'Administrador'),
        ('customer', 'Cliente'),
        ('producer', 'Produtor'),
    )
    profile_type = models.CharField(max_length=10, default='customer', choices= PROFILE_TYPE_CHOICES )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')

class ServiceAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False) 
    state = models.CharField(max_length=2, null=False, blank=False)

class DeliveryTime(models.Model):
    DAYS = (
        ('monday', 'Segunda-feira'),
        ('tuesday', 'Terça-feira'),
        ('wednesday', 'Quarta-feira'),
        ('thursday', 'Quinta-feira'),
        ('friday', 'Sexta-feira'),
        ('saturday', 'Sábado'),
        ('sunday', 'Domingo'),
    )
    service_address = models.ForeignKey(ServiceAddress, on_delete=models.CASCADE, null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    day = models.CharField(max_length=15, null=False, blank=False, choices=DAYS)

