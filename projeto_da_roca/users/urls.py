from django.urls import path
from .views import list_users, create_users, DeliveryTimeView, ServiceAddressView

urlpatterns = [
    path('', list_users),
    path('costumer/create', create_users, name='create_customer'),
    path('delivery_time/list', DeliveryTimeView.list_delivery_time, name='list_delivery_time'),
    path('delivery_time/create', DeliveryTimeView.create_delivery_time, name='create_delivery_time'),
    path('delivery_time/delete', DeliveryTimeView.delete_delivery_time, name='delete_delivery_time'),

    path('service_address/list', ServiceAddressView.list_service_address, name='list_service_address'),
    path('service_address/create', ServiceAddressView.create_service_address, name='create_service_address'),
    path('service_address/delete', ServiceAddressView.delete_service_address, name='delete_service_address'),
]
