"""
A module for handling the bot-checking loop in the background
without leaving the application hanging.
"""

from io import StringIO

from celery import shared_task
import pandas as pd

from .checker import check_for_bots

@shared_task(bind=True)
def check_for_bots_task(self, essay_list, data, check):
    """
    Handles the logic for bot checks using Celery
    instead of Django.
    """
    print("CELERY TASK STARTED")
    data = pd.read_csv(StringIO(data))
    check_for_bots(self, essay_list, data, check)
    data = data.to_csv(index=False)
    return data
