import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vobla_vpn.settings')

app = Celery('coffee_house')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
