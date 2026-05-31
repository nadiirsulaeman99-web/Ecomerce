from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name= 'order_create' ),
    path('success/<str:order_id>/', views.order_success, name= 'order_success' ),
    path('admin/pdf/<int:order_id>/', views.admin_order_pdf, name= 'admin_order_pdf')
    
]
