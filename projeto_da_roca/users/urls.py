from django.urls import path
from .views import list_users, create_users, DeliveryTimeView

urlpatterns = [
    path('', list_users),
    path('costumer/create', create_users, name='create_customer'),
    path('delivery_time/list', DeliveryTimeView.list_delivery_time, name='list_delivery_time'),
    path('delivery_time/create', DeliveryTimeView.create_delivery_time, name='create_delivery_time'),
    path('delivery_time/delete', DeliveryTimeView.delete_delivery_time, name='delete_delivery_time'),
]
