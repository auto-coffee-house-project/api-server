from django.urls import path

from gifts.views import GiftActivateApi, GiftListCreateApi

app_name = 'gifts'
urlpatterns = [
    path(
        r'users/<int:client_user_id>/',
        GiftListCreateApi.as_view(),
        name='list-create',
    ),
    path(r'activate/', GiftActivateApi.as_view(), name='activate'),
]
