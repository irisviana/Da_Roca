from django.urls import path
from .views import list_users, create_users, DeliveryTimeView

urlpatterns = [
    path('', list_users),
    path('cadastro_cliente/', create_users, name='cadastro_cliente'),
    path('delivery_time/listar', DeliveryTimeView.list_delivery_time, name='delivery_time-listar'),
    path('delivery_time/cadastro', DeliveryTimeView.create_delivery_time, name='delivery_time-cadastro'),
    path('delivery_time/deletar', DeliveryTimeView.delete_delivery_time, name='delivery_time-deletar'),
]
