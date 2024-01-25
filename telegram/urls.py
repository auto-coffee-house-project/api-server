from django.urls import path, include

from telegram.views import UserCreateUpdateApi, BotListApi, UserRetrieveApi

app_name = 'telegram'

bots_urlpatterns = [
    path(
        r'',
        BotListApi.as_view(),
        name='bot-list',
    )
]

users_urlpatterns = [
    path(
        r'',
        UserCreateUpdateApi.as_view(),
        name='user-create',
    ),
    path(
        r'<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='user-retrieve',
    )
]

urlpatterns = [
    path('bots/', include(bots_urlpatterns)),
    path('users/', include(users_urlpatterns)),
]
