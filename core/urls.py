from django.urls import path

from core.views import ping_view

urlpatterns = [
    path(r'ping/', ping_view, name='ping'),
]
