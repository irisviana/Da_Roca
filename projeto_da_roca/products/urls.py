from django.urls import path

from .views import ProductView

urlpatterns = [
    path('products/list', ProductView.list_products, name='list_products'),
    path('create', ProductView.create_product, name='create_product'),
    path('products/update/<int:product_id>', ProductView.update_product,
         name='update_product'),
    path('products/delete', ProductView.delete_product,
         name='delete_product'),

]
