from django.urls import path, include

from telegram.views import (
    UserRetrieveCreateUpdateApi,
    BotListApi,
    BotRetrieveUpdateApi,
)

app_name = 'telegram'

bots_urlpatterns = [
    path(
        r'',
        BotListApi.as_view(),
        name='bot-list',
    ),
    path(
        r'<int:bot_id>/',
        BotRetrieveUpdateApi.as_view(),
        name='bot-retrieve',
    )
]

urlpatterns = [
    path('bots/', include(bots_urlpatterns)),
    path(
        r'users/',
        UserRetrieveCreateUpdateApi.as_view(),
        name='user-retrieve-create-update',
    ),
]
