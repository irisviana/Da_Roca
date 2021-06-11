from django.urls import path

from .views import ProductView, CategoryView

urlpatterns = [
    path('products/list', ProductView.list_products, name='list_products'),
    path('create', ProductView.create_product, name='create_product'),
    path('products/update/<int:product_id>', ProductView.update_product, name='update_product'),
    path('products/delete', ProductView.delete_product, name='delete_product'),
    path('categories/list', CategoryView.list_categories, name='list_categories'),
    path('categories/create', CategoryView.create_category, name='create_category'),
    path('categories/update/<int:category_id>', CategoryView.update_category, name='update_category'),
    path('categories/delete', CategoryView.delete_category, name='delete_category'),
]
