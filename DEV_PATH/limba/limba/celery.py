import os
from celery import Celery
# from celery.schedules import crontab
# from datetime import timedelta
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'limba.settings')

app = Celery('Scanner')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'db_trassir_1s': {
        'task': 'Main.tasks.test_function',
        'schedule': 1.0
    }
}
app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()