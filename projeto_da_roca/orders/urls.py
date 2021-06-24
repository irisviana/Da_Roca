from django.urls import path

from .views import CartProductView
from .views import ConfirmOrderView


urlpatterns = [
    path('cart/', CartProductView.list, name='cart'),
    path('cart/create', CartProductView.create, name='create-cart'),
    path('cart/update', CartProductView.update, name='update-cart'),
    path('cart/delete', CartProductView.delete, name='remove-cart'),
    path('confirm/', ConfirmOrderView.list, name='confirm-order'),

]
