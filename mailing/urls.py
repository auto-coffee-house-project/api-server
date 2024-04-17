from django.urls import path

from mailing.views import MailingCreateApi

urlpatterns = [
    path(r'', MailingCreateApi.as_view()),
]
