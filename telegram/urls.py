from django.urls import path

from telegram.views import UserCreateApi, UserRetrieveApi

urlpatterns = [
    path(
        r'users/',
        UserCreateApi.as_view(),
        name='user-create',
    ),
    path(
        r'users/<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='user-retrieve',
    ),
]
