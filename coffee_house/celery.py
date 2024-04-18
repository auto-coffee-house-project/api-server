import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_house.settings')

app = Celery('coffee_house')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'remove-expired-sale-codes': {
        'task': 'shops.tasks.remove_expired_sale_codes',
        'schedule': 600,
    },
    'remove-expired-employee-invitations': {
        'task': 'shops.tasks.remove_expired_invitations',
        'schedule': 600,
    },
    'remove-expired-employee-requests': {
        'task': 'gifts.tasks.remove_expired_gifts',
        'schedule': 600,
    },
}
