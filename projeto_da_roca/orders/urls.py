from django.urls import path

from .views import CartProductView
from .views import ConfirmOrderView
from .views import SellerOrderView

urlpatterns = [
    path('cart/', CartProductView.list, name='cart'),
    path('cart/create', CartProductView.create, name='create-cart'),
    path('cart/update', CartProductView.update, name='update-cart'),
    path('cart/delete', CartProductView.delete, name='remove-cart'),
    path('confirm/', ConfirmOrderView.list, name='confirm-order'),
    path('seller/', SellerOrderView.list, name='seller-orders'),
    path('seller/datails', SellerOrderView.index, name='seller-order-detail'),
    path('cancel/<int:order_id>', SellerOrderView.cancel, name='cancel-order'),
    path('update/status/<int:order_id>', SellerOrderView.update, name='update-status-order'),

]
