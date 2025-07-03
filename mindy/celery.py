# mindy/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mindy.settings")

app = Celery("mindy")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


CELERY_BROKER_URL = "rediss://default:AZgTAAIjcDE1YjU0YWRkNmE2Zjk0ZWQwYjM0ZWI5MDFmZmRkN2Y2MXAxMA@first-polliwog-38931.upstash.io:6379"


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
