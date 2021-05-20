from django.urls import path
from .views import list_users, cadastro_cliente, HorarioEntregaView

urlpatterns = [
    path('', list_users),
    path('cadastro_cliente/', cadastro_cliente, name='cadastro_cliente'),
    path('horarioentrega/listar', HorarioEntregaView.listarHorarioEntrega, name='horarioentrega-listar'),
]
