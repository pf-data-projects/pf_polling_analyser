from io import BytesIO, StringIO

import pandas as pd

from celery.result import AsyncResult

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from .forms import BotCheckForm
from .helpers import get_questions
from .checker import check_for_bots
from .tasks import check_for_bots_task


def upload_bots(request):
    """
    A function to handle uploading data
    and passing it to bot checking algorithm.
    """
    if request.method == 'POST':
        # handle unauth users
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this feature")
            return redirect(reverse('home'))
        form = BotCheckForm(request.POST, request.FILES)
        if form.is_valid():
            email = request.user.email
            survey_data = request.FILES['data_file']
            survey_id = form.cleaned_data['survey_id']
            check = form.cleaned_data['check']
            data = pd.read_excel(survey_data, header=0, sheet_name="Sheet1")
            # get questions from API.
            essay_list = get_questions(survey_id)

            # hand over to celery to do checks.
            data = data.to_csv(index=False)
            data = check_for_bots_task.delay(email, essay_list, data, check)

            # cache task id to fetch later.
            cache.set('bot_task_id', data.id, 3600)
            messages.success(
                request,
                "Bot check underway. PLEASE DO NOT RESUBMIT THE FORM OR YOU MAY MAKE JEREMY CRY"
            )
            return redirect(reverse('bot_check'))
        else:
            message = """
            There was a problem with your form submission. 
            Please check the data and try again
            """
            messages.error(request, message)
            return redirect(reverse('bot_check'))
    else:
        form = BotCheckForm()

    return render(
        request,
        'bot_check_form.html',
        {'form': form}
    )


def fetch_checks(request):
    """
    A view to handle fetching checked data from the
    celery result backend.
    """
    task_id = cache.get('bot_task_id')
    try:
        result = AsyncResult(task_id)
    except ValueError as e:
        print(e)
        messages.error(
            request,
            """ 
            No data was found. Either the checks have not yet
            been completed or too much time has elapsed since 
            they were run.
            """
        )
        return redirect('bot_check')
    print("fetching results")
    if result.ready():
        data = result.get()
        df = pd.read_csv(StringIO(data))
        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        response = HttpResponse(
            excel_buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
        )
        response['Content-Disposition'] = 'attachment; filename="checked.xlsx"'
        return response
    else:
        print("Checks are still processing. Please wait.")
        messages.error(
            request,
            "Bot checks are still processing. Please wait."
        )
        return redirect('bot_check')


def task_status(request):
    """
    A function to poll the bot checking celery worker
    to log task progress.
    """
    task_id = cache.get('bot_task_id')

    # handle no checks running.
    if task_id is None:
        return JsonResponse({
            'status': 'No bot checks have been run yet',
            'details': 'No bot checks have been run yet',
            'result': "No results yet..."
        })

    # query task.
    task_result = AsyncResult(task_id)

    # handle error/failed task.
    if task_result.state == 'FAILURE':
        return JsonResponse({
            'status': 'FAILURE',
            'details': str(task_result.result),
            'traceback': task_result.traceback,
        })

    # Return data about task.
    return JsonResponse({
        'status': task_result.state,
        'details': 'Result ready to download' if task_result.ready() else task_result.info,
        'result': 'Result ready to download' if task_result.ready() else "still working..."
    })
