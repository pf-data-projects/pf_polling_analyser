"""
A module containing tasks for celery to do in the background.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ standard library
from io import StringIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django.core.mail import send_mail
from celery import shared_task
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from queries.table_calculations.calculate_totals import table_calculation


@shared_task(bind=True)
def handle_crossbreaks(
    self, email, data, question_data, standard_cb, non_standard_cb):
    """
    This handles the crossbreak logic
    in a separate celery worker.
    """

    data = pd.read_csv(StringIO(data))
    question_data = pd.read_csv(StringIO(question_data))

    # try:
    table = table_calculation(self, data, question_data, standard_cb, non_standard_cb)
    table[0] = table[0].to_csv(index=None)
    try:
        send_mail(
            'Your Crossbreaks Have Been Completed',
            """
            Your crossbreak processing has finished. 
            Please make sure you download them 
            in the next few minutes before they expire.
            """,
            'jeremy.simons@publicfirst.co.uk',
            [email],
            fail_silently=False
        )
    except Exception as e:
        print("Sending mail failed:", {e})

    # return table
    return {"table": table[0], "json": table[1]}
