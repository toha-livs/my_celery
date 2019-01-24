# -*- coding: utf-8 -*-
# http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_test.settings')

app = Celery('celery_test')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'main.tasks.display_time',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'add-every-3-minutes': {
        'task': 'main.tasks.hook_olx_data',
        'schedule': crontab(minute='1, 3, 7, 10, 12'),
        'args': ('планшет',)
    },
}
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

