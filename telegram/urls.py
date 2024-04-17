from django.urls import path

from telegram.views import (
    BotListApi,
    BotRetrieveUpdateApi,
    UserCreateUpdateApi,
    UserRetrieveApi,
)

app_name = 'telegram'

urlpatterns = [
    path(
        'bots/',
        BotListApi.as_view(),
        name='bot-list',
    ),
    path(
        r'bots/me/',
        BotRetrieveUpdateApi.as_view(),
        name='bot-retrieve-update',
    ),
    path(
        r'users/',
        UserCreateUpdateApi.as_view(),
        name='user-create-update',
    ),
    path(
        r'users/<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='user-retrieve',
    ),
]
