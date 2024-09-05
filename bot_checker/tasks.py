"""
A module for handling the bot-checking loop in the background
without leaving the application hanging.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
from io import StringIO

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.core.mail import send_mail
from celery import shared_task
import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .checker import check_for_bots

@shared_task(bind=True)
def check_for_bots_task(self, email, essay_list, data, check):
    """
    Handles the logic for bot checks using Celery
    instead of Django.
    """
    # print("CELERY TASK STARTED")
    data = pd.read_csv(StringIO(data))
    check_for_bots(self, essay_list, data, check)
    data = data.to_csv(index=False)

    # email notification
    try:
        send_mail(
            'Your bot check has been completed',
            """
            Your bot check has been completed. Please
            make sure that you download the checked
            data in the next few minutes before they
            expire.
            """,
            'jeremy.simons@publicfirst.co.uk',
            [email],
            fail_silently=False
        )
    except Exception as e:
        print(f"sending mail failed: {e}")
    return data
