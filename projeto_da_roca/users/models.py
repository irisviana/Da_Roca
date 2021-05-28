from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    sale_description = models.TextField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.username = uuid.uuid4().hex[:30]
        super().save(*args, **kwargs)


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



class ServiceAddress(models.Model):
    STATES = (
        ('AC','Acre'),
        ('AL','Alagoas'),
        ('AP','Amapá'),
        ('AM','Amazonas'),
        ('BA','Bahia'),
        ('CE','Ceará'),
        ('DF','Distrito Federal'),
        ('ES','Espírito Santo'),
        ('GO','Goiás'),
        ('MA','Maranhão'),
        ('MT','Mato Grosso'),
        ('MS','Mato Grosso do Sul'),
        ('MG','Minas Gerais'),
        ('PA','Pará'),
        ('PB','Paraíba'),
        ('PR','Paraná'),
        ('PE','Pernambuco'),
        ('PI','Piauí'),
        ('RJ','Rio de Janeiro'),
        ('RN','Rio Grande do Norte'),
        ('RS','Rio Grande do Sul'),
        ('RO','Rondônia'),
        ('RR','Roraima'),
        ('SC','Santa Catarina'),
        ('SP','São Paulo'),
        ('SE','Sergipe'),
        ('TO','Tocantins'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False, choices=STATES, default=STATES[0])


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
    service_address = models.ForeignKey(ServiceAddress, on_delete=models.CASCADE, null=True, blank=True)
    time = models.TimeField(null=False, blank=False)
    day = models.CharField(max_length=15, null=False, blank=False, choices=DAYS, default=DAYS[0])

