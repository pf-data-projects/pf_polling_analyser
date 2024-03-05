"""
A module containing tasks for celery to do in the background.
"""

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ standard library
from io import BytesIO, StringIO
from time import sleep

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from celery import shared_task
from django.core.cache import cache
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .logic import extra_logic
from . import weight as wgt
from queries.table_calculations.calculate_totals import table_calculation


@shared_task(bind=True)
def handle_weighting(
    self, user_id, survey_data, weight_proportions, apply, custom,
    questions=None, groups=None, standard_weights=None):
    """
    Called by weighting view.

    Effectively passes all the weighting 
    functionality to a celery task.
    """
    print("handling weighting")
    # survey_data = pd.read_json(survey_data)
    survey_data = pd.read_csv(StringIO(survey_data))
    # weight_proportions = pd.read_json(weight_proportions)
    weight_proportions = pd.read_csv(StringIO(weight_proportions))


    if apply and not custom:
        try:
            weighted_data = wgt.run_weighting(survey_data, weight_proportions)
        except StopIteration:
            message="""
                An error occurred searching for the Socio-Economic Grade question.
                The code couldn't find it - Have you checked that this question exists in the data,
                or that the wording hasn't changed?
                """
            print(message)
            raise
        except Exception as e:
            message=f"""
                There was an error in the weighting calculation.
                Please make sure the questions/columns in the data
                match the groups specified in the weight proportions.

                This is the error the code returned: {e}
                """
            print(message)
            raise

    # ~~~~~~~~~~~~~~~~ Run ipf module for custom weights
    elif custom:
        try:
            weighted_data = wgt.apply_custom_weight(
                survey_data, weight_proportions, questions, groups, standard_weights
            )
        except StopIteration:
            message="""
                An error occurred searching for the Socio-Economic Grade question.
                The code couldn't find it - Have you checked that this question exists in the data,
                or that the wording hasn't changed?
                """
            print(message)
            raise
        except Exception as e:
            message=f"""
                There was an error in the weighting calculation.
                Please make sure the questions/columns in the data
                match the groups specified in the weight proportions.

                This is the error the code returned: {e}
                """
            print(message)
            raise

    # ~~~~~~~~~~~~~~~~ Run ipf module for no weights
    else:
        weighted_data = wgt.apply_no_weight(survey_data)

    # Save the data to django's cache.
    # excel_buffer = BytesIO()
    # weighted_data.to_excel(excel_buffer, index=False)
    # excel_buffer.seek(0)
    # unique_id = "weights_for_user_" + str(user_id)
    # cache.set(unique_id, excel_buffer.getvalue(), 300)
    result = weighted_data.to_csv(index=False)
    # print(f"this is the result: {result}")
    return result


@shared_task(bind=True)
def handle_crossbreaks(
    self, data, question_data, standard_cb, non_standard_cb):
    """
    This handles the crossbreak logic
    in a separate celery worker.
    """

    data = pd.read_csv(StringIO(data))
    question_data = pd.read_csv(StringIO(question_data))

    try:
        table = table_calculation(self, data, question_data, standard_cb, non_standard_cb)
        table[0] = table[0].to_csv(index=None)
        # return table
        return {"table": table[0], "json": table[1]}

    except (KeyError, IndexError) as e:
        message = f"""
            There was an error when running this code for crossbreaks.
            The most likely cause of this error is entering a crossbreak that
            doesn't exist in the data.

            It could also be caused by changes in the wording of standard crossbreak
            questions.

            Here is the content of the error message: {e}
            """
        print(message)
        self.update_state(
            status="FAILURE",
            meta={"Error message": message}
        )
        return message
