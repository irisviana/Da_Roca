from django.urls import path

from .views import list_users, create_users, DeliveryTimeView, ServiceAddressView,admin_home,list_admin,add_admin

urlpatterns = [
    path('', list_users),
    path('create', create_users, name='create_customer'),
    path('delivery_time/list/<int:service_address_id>', DeliveryTimeView.list_delivery_time, name='list_delivery_time'),
    path('delivery_time/create/<int:service_address_id>', DeliveryTimeView.create_delivery_time, name='create_delivery_time'),
    path('delivery_time/delete/', DeliveryTimeView.delete_delivery_time, name='delete_delivery_time'),
    path('delivery_time/update/<int:delivery_time_id>', DeliveryTimeView.update_delivery_time, name='update_delivery_time'),
    path('service_address/list', ServiceAddressView.list_service_address, name='list_service_address'),
    path('service_address/create', ServiceAddressView.create_service_address, name='create_service_address'),
    path('service_address/delete', ServiceAddressView.delete_service_address, name='delete_service_address'),
    path('service_address/update/<int:service_address_id>', ServiceAddressView.update_service_address, name='update_service_address'),
    path('admin/', admin_home, name='home_admin'),
    path('admin/manage_admin', list_admin, name='manage_admin'),
    path('admin/add', add_admin, name='admin_add'),
]
