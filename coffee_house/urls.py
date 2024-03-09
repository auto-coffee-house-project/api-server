from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/shops/', include('shops.urls')),
    path('api/telegram/', include('telegram.urls')),
    path('api/mailing/', include('mailing.urls')),
]
