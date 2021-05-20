from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Usuario(AbstractUser):
    cpf = models.CharField(max_length=11, null=True, blank=True)
    numeroTelefone = models.CharField(max_length=50, null=True, blank=True)


class Endereco(models.Model):
    OPCOES_TIPO_ENDERECO = (
        ('usuario', 'Usuário'),
        ('order', 'Pedido'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    tipoEndereco = models.CharField(max_length=10, default='user', choices=OPCOES_TIPO_ENDERECO)
    cep = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    rua = models.CharField(max_length=100, null=True, blank=True)
    numeroCasa = models.CharField(max_length=10, null=True, blank=True)

class Perfil(models.Model):
    OPCOES_TIPO_PERFIL = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('produtor', 'Produtor'),
    )
    tipoPerfil = models.CharField(max_length=10, default='cliente', choices= OPCOES_TIPO_PERFIL )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='perfil')


class EnderecoAtendimento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, blank=False)
    cidade = models.CharField(max_length=50, null=False, blank=False)
    estado = models.CharField(max_length=2, null=False, blank=False)

class HorarioEntrega(models.Model):
    DIAS = (
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    )
    enderecoAtendimento = models.ForeignKey(EnderecoAtendimento, on_delete=models.CASCADE, null=False, blank=False)
    hora = models.TimeField(null=False, blank=False)
    dia = models.CharField(max_length=15, null=False, blank=False, choices=DIAS)

