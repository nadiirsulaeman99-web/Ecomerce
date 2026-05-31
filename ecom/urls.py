from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static
from acounts import views as acounts_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Store.urls', namespace='Store')),
    path('acounts/', include('acounts.urls', namespace='acounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('accounts/activate/<str:uidb64>/<str:token>/', acounts_views.activate_account, name='activate_direct_root'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
