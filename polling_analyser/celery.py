"""Instantiate a celery object to be our worker."""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polling_analyser.settings')
app = Celery('polling_analyser')
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
