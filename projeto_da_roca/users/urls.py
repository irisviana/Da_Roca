from django.urls import path

from .views import DeliveryTimeView
from .views import ServiceAddressView
from .views import UserView
from .views import AddressView
from .views import costumer_home

urlpatterns = [
    path('', UserView.list_users),
    path('create', UserView.create_users, name='create_customer'),
    path('<str:username>/update', UserView.update_users, name='update_customer'),
    path('<str:username>/address/create', AddressView.create_address, name='create_customer_address'),
    path('delivery_time/list/<int:service_address_id>', DeliveryTimeView.list_delivery_time, name='list_delivery_time'),
    path('delivery_time/create/<int:service_address_id>', DeliveryTimeView.create_delivery_time, name='create_delivery_time'),
    path('delivery_time/delete/', DeliveryTimeView.delete_delivery_time, name='delete_delivery_time'),
    path('delivery_time/update/<int:delivery_time_id>', DeliveryTimeView.update_delivery_time, name='update_delivery_time'),
    path('service_address/list', ServiceAddressView.list_service_address, name='list_service_address'),
    path('service_address/create', ServiceAddressView.create_service_address, name='create_service_address'),
    path('service_address/delete', ServiceAddressView.delete_service_address, name='delete_service_address'),

    path('costumer-home', costumer_home, name='costumer_home'),
]
