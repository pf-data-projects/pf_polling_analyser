"""
A module containing tasks for celery to do in the background.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ standard library
from io import StringIO

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from celery import shared_task
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from queries.table_calculations.calculate_totals import table_calculation


@shared_task(bind=True)
def handle_crossbreaks(
    self, data, question_data, standard_cb, non_standard_cb):
    """
    This handles the crossbreak logic
    in a separate celery worker.
    """

    data = pd.read_csv(StringIO(data))
    question_data = pd.read_csv(StringIO(question_data))

    # try:
    table = table_calculation(self, data, question_data, standard_cb, non_standard_cb)
    table[0] = table[0].to_csv(index=None)
    # return table
    return {"table": table[0], "json": table[1]}
