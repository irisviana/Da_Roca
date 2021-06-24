from django.urls import path

from .views import CartProductView

urlpatterns = [
    path('cart/', CartProductView.list, name='cart'),
    path('cart/create', CartProductView.create, name='create-cart'),
    path('cart/update', CartProductView.update, name='update-cart'),
    path('cart/delete', CartProductView.delete, name='remove-cart'),
]
