"""
This file handles the logic for the pages associated with this
app; the weighting and crossbreaks forms and their respective logic.

1. weight_data is a function that either displays the empty form
or submits data depending on whether the request method is
POST or GET.

2. upload_csv is a function that similarly either displays
the empty form if the request method is GET, and handles
calculations if the request method us POST.

3. download_csv is a function that downloads the output of
the crossbreak calculations on the user's machine if it
exists in the cache, else display a message saying it's 
not there

4. download_weights is a function that downloads the
weighted data if it exists, or displays a message
if not.
"""

from io import BytesIO
import json
import os

import pandas as pd
from docx import Document

from django.shortcuts import render, redirect, reverse
from .forms import CSVUploadForm, WeightForm, CrossbreakFormSet
from django.core.cache import cache
from django.http import HttpResponse

from .clean_data.clean_survey_legend import clean_survey_legend
from .clean_data.clean_order import clean_order

from queries.table_calculations.calculate_totals import table_calculation
from queries.api_request.get_survey_questions import get_questions_json
from queries.api_request.get_processed_questions import (
    extract_questions_from_pages,
    extract_data_from_question_objects
)
from . import weight as wgt

def weight_data(request):
    """
    A view that:
    1. renders the weighting form.
    2. processes the data submitted in the weight form.
    3. calls the run_weighting function if it's valid and if the
    user has selected to weight it.
    4. calls the apply_no_weight function if the user
    has not selected to weight the data.
    """
    if request.method == 'POST':
        form = WeightForm(request.POST, request.FILES)
        if form.is_valid():
            # Fetches data from form & converts them to df
            survey_data = request.FILES['results']
            survey_data = pd.read_excel(survey_data, header=0, sheet_name="Worksheet")
            weight_proportions = request.FILES['weights']
            weight_proportions = pd.read_excel(weight_proportions, header=0, sheet_name="Sheet1")
            apply = form.cleaned_data['apply_weights']

            # Run ipf module
            if apply:
                weighted_data = wgt.run_weighting(survey_data, weight_proportions)

            else:
                weighted_data = wgt.apply_no_weight(survey_data)

            # Cache the weighted data to be downloaded by user later
            excel_buffer = BytesIO()
            weighted_data.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            unique_id = "weights_for_user_" + str(request.user.id)
            cache.set(unique_id, excel_buffer.getvalue(), 300)
            print("Weighting SUCCESS!!")
            return redirect(reverse('home'))
    else:
        form = WeightForm()

    return render(request, 'weight_form.html', {
        'form': form,
    })

def upload_csv(request):
    """
    A view that:
    1. renders the csv upload for.
    2. restrict unauthorised users.
    3. processes form data.
    4. If form data is valid, it calls the API with survey ID supplied
    by the user.
    5. calls function to process data returned by API
    6. runs table calculation passing in user-submitted data as well 
    as data from API.
    7. Return the empty form when all this is complete.
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            print('You are not logged in to the PF polling analyser.')
            print('You cannot make this request until you log in.')
            return HttpResponse(
                "You are not logged in. Please log in to use this feature"
            )
        form = CSVUploadForm(request.POST, request.FILES)
        formset = CrossbreakFormSet(request.POST, prefix="crossbreaks")
        if form.is_valid() and formset.is_valid():
            data_file = request.FILES['data_file']
            survey_id = form.cleaned_data['survey_id']
            standard_cb = form.cleaned_data['standard_cb']
            non_standard_cb = []
            num_submitted_forms = 0
            for form in formset:
                if form.has_changed():
                    num_submitted_forms += 1
            if num_submitted_forms > 0:
                for sub_form in formset:
                    cb_name = sub_form.cleaned_data['non_standard_cb_name']
                    cb_question = sub_form.cleaned_data['non_standard_cb_question']
                    cb_answer = sub_form.cleaned_data['non_standard_cb_answer']
                    cb_data = [cb_name, cb_question, cb_answer]
                    non_standard_cb.append(cb_data)

            # convert the data to python-readable formats
            data = pd.read_excel(data_file, header=0, sheet_name="Sheet1")

            # get question data from API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # JSON AND CSV OUTPUT CURRENTLY COMMENTED OUT FOR PERFORMANCE
            survey_questions = get_questions_json(survey_id)
            questions = extract_questions_from_pages(survey_questions)
            # with open("questions_list.json", "w") as outfile:
            #     json.dump(survey_questions, outfile, indent=2)
            question_data = extract_data_from_question_objects(questions)
            # question_data.to_csv(
            #     "question_data.csv", index=False, encoding="utf-8-sig")

            # Run calculations
            table = table_calculation(data, question_data, standard_cb, non_standard_cb)

            # Store results in cache
            csv_buffer = BytesIO()
            table.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_buffer.seek(0)
            unique_id = "csv_for_user_" + str(request.user.id)
            cache.set(unique_id, csv_buffer.getvalue(), 300)
            print("SUCCESS!!")

            # Redirect user to homepage.
            return redirect(reverse('home'))
    else:
        form = CSVUploadForm()
        formset = CrossbreakFormSet(prefix="crossbreaks")

    return render(request, 'upload_form.html', {
        'form': form,
        'formset': formset
    })

def download_csv(request):
    """
    Handles retrieval of cached output table.
    """
    unique_id = "csv_for_user_" + str(request.user.id)
    csv_data = cache.get(unique_id)
    if csv_data:
        response = HttpResponse(csv_data, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="table.csv"'
        return response
    else:
        return HttpResponse("CSV NOT FOUND")

def download_weights(request):
    """
    Handles retrieval of cached weighted data.
    """
    unique_id = "weights_for_user_" + str(request.user.id)
    excel_data = cache.get(unique_id)
    if excel_data:
        response = HttpResponse(
            excel_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
        )
        response['Content-Disposition'] = 'attachment; filename="weighted_data.xlsx"'
        return response
    else:
        return HttpResponse("WEIGHTS NOT FOUND")
