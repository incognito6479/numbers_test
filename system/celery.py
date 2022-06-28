from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from system.settings import CELERY_BEAT_GET_SHEET_DATA_RUN_TIME


"""
Celery settings
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system.settings')
app = Celery('system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


"""

This code runs every 15 seconds gets data from Google API
and adds to the DB

TZ Part 3

"""
app.conf.beat_schedule = {
    'run-every-15-seconds': {
        'task': 'mainapp.tasks.test_celery',
        'schedule': CELERY_BEAT_GET_SHEET_DATA_RUN_TIME
    }
}
