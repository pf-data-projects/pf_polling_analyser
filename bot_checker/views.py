from io import BytesIO

import pandas as pd

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse

from .forms import BotCheckForm
from .helpers import get_questions
from .checker import check_for_bots


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
        print(form.is_valid)
        if form.is_valid():
            print("calling alchemer...")
            survey_data = request.FILES['data_file']
            survey_id = form.cleaned_data['survey_id']
            check = form.cleaned_data['check']
            data = pd.read_excel(survey_data, header=0, sheet_name="Sheet1")
            # get questions from API
            essay_list = get_questions(survey_id)
            print("starting checks...")
            data = check_for_bots(essay_list, data, check)

            excel_buffer = BytesIO()
            data.to_excel(excel_buffer, index=False)
            unique_id = "bot_checks_for_user_" + str(request.user.id)
            cache.set(unique_id, excel_buffer.getvalue(), 300)
            response = HttpResponse(
                excel_buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
            )
            response['Content-Disposition'] = 'attachment; filename="checked_data.xlsx"'
            return response
        else:
            print("form submission invalid")
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
