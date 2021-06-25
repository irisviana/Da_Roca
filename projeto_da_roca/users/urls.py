from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import UserView, AddressView, DeliveryTimeView, ServiceAddressView, OrderView

urlpatterns = [
    path('create', UserView.create_users, name='create_customer'),
    path('update', UserView.update_users, name='update_customer'),
    path('update/email', UserView.update_email_user, name='update_email_customer'),
    path('update/password', UserView.update_password_user, name='update_password_customer'),

    path('delete', UserView.self_delete, name='self_delete'),
    path('address/create', AddressView.create_address, name='create_customer_address'),
    path('address/list', AddressView.list_address, name='list_customer_address'),

    path('address/delete', AddressView.delete_address, name='delete_address'),
    path('address/update/<int:address_id>', AddressView.update_address,
         name='update_address'),

    path('delivery_time/list/<int:service_address_id>', DeliveryTimeView.list_delivery_time, name='list_delivery_time'),
    path('delivery_time/create/<int:service_address_id>', DeliveryTimeView.create_delivery_time,
         name='create_delivery_time'),
    path('delivery_time/delete/', DeliveryTimeView.delete_delivery_time, name='delete_delivery_time'),
    path('delivery_time/update/<int:delivery_time_id>', DeliveryTimeView.update_delivery_time,
         name='update_delivery_time'),

    path('service_address/list', ServiceAddressView.list_service_address, name='list_service_address'),
    path('service_address/create', ServiceAddressView.create_service_address, name='create_service_address'),
    path('service_address/delete', ServiceAddressView.delete_service_address, name='delete_service_address'),
    path('service_address/update/<int:service_address_id>', ServiceAddressView.update_service_address,
         name='update_service_address'),
    path('order/list', OrderView.list_order, name='list_user_orders'),

    path('customer_home_first', UserView.customer_home_first, name='customer_home_first'),
    path('admin/', UserView.admin_home, name='home_admin'),
    path('admin/users/<str:user_type>', UserView.list_users, name='manage_user'),
    path('admin/users', UserView.list_users, name='manage_user'),
    path('admin/add', UserView.add_admin, name='admin_add'),
    path('admin/remove_admin', UserView.remove_admin, name='admin_remove'),
    path('admin/user/delete', UserView.delete_user, name="delete_user"),

    path('customer_home', UserView.customer_home, name='customer_home'),
    path('customer_home_search_seller', UserView.search_seller, name='search_sellers'),
    path('seller/', UserView.seller_home, name='home_seller'),
    path('seller/updateStoreStatus', UserView.update_users_store_status, name='store_status_update'),
    path('seller/request', UserView.request_seller, name='seller_request'),
    path('seller/manage_seller', UserView.manage_seller, name='seller_manage'),
    path('seller/view_seller_request/<int:user_id>', UserView.view_seller_request, name='view_request_seller'),
    path('seller/refuse_seller_request', UserView.refuse_seller_request, name='refuse_request_seller'),
    path('seller/approve_seller_request', UserView.approve_seller_request, name='approve_request_seller'),
    path('seller/make_admin', UserView.make_admin, name='admin_make'),
    path('seller/view/<int:user_id>', UserView.view_seller, name='view_seller'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA__PRODUCT_URL,
                          document_root=settings.MEDIA_PRODUCT_ROOT)
