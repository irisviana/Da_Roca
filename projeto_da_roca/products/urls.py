from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import ProductView, CategoryView, FavoriteView


urlpatterns = [
    path('products/list', ProductView.list_products, name='list_products'),
    path('products/see', ProductView.see_products, name='see_products'),
    path('products/admin', ProductView.search_product_to_admin, name='search_products_admin'),
    path('create', ProductView.create_product, name='create_product'),
    path('customer_home_search_product', ProductView.search_product, name='search_products'),
    path('products/update/<int:product_id>', ProductView.update_product, name='update_product'),
    path('products/delete', ProductView.delete_product, name='delete_product'),
    path('products/view/<int:product_id>', ProductView.view_product, name='view_product'),
    path('categories/list', CategoryView.list_categories, name='list_categories'),
    path('categories/create', CategoryView.create_category, name='create_category'),
    path('categories/update/<int:category_id>', CategoryView.update_category, name='update_category'),
    path('categories/delete', CategoryView.delete_category, name='delete_category'),
    path('favorites/create', FavoriteView.create_favorite, name='create_favorite'),
    path('favorites/list', FavoriteView.list_favorites, name='list_favorites'),
    path('favorites/delete', FavoriteView.delete_favorite, name='delete_favorite'),
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA__PRODUCT_URL ,
                              document_root=settings.MEDIA_PRODUCT_ROOT)
