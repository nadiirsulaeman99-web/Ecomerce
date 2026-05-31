from django.urls import path
from . import views


app_name = 'acounts'
urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    # path('accounts/activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_acount'),
    
]
