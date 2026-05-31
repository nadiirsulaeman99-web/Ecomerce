from django.urls import path
from .views import home, product_detail, search

app_name = 'Store'

urlpatterns = [
    path('', home , name='home'  ),
    path('category/<slug:category_slug>', home, name='products_by_category'),
    path('product/<slug:product_slug>/', product_detail, name='product_detail' ),
    path('search/', search, name='product_search'),

]
