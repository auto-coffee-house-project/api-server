from django.urls import path, include

from telegram.views import UserCreateApi, UserRetrieveApi, BotListApi

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
        UserCreateApi.as_view(),
        name='user-create',
    ),
    path(
        r'<int:user_id>/',
        UserRetrieveApi.as_view(),
        name='user-retrieve',
    ),
]

urlpatterns = [
    path('bots/', include(bots_urlpatterns)),
    path('users/', include(users_urlpatterns)),
]
