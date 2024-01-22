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

5. GuideView handles logic to get the instructions page.
"""

from io import BytesIO
import re
import json
import os

import pandas as pd

from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from .forms import CSVUploadForm, WeightForm, CrossbreakFormSet, CustomWeightFormSet
from django.core.cache import cache
from django.http import HttpResponse

from queries.table_calculations.calculate_totals import table_calculation
from queries.api_request.get_survey_questions import get_questions_json
from queries.api_request.get_processed_questions import (
    extract_questions_from_pages,
    extract_data_from_question_objects
)
from . import weight as wgt

from . import validation as vld

class GuideView(View):
    """
    A view to handle the guide/instructions page.
    """
    def get(self, request):
        """
        Gets the guide page.
        """
        return render(request, "guide.html")

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
        formset = CustomWeightFormSet(request.POST, prefix="weights") 
        if form.is_valid():
            # Handles all the form data
            survey_data = request.FILES['results']
            survey_data = pd.read_excel(survey_data, header=0, sheet_name="Worksheet")
            survey_data.columns = [preprocess_header(col) for col in survey_data.columns]
            weight_proportions = request.FILES['weights']
            weight_proportions = pd.read_excel(weight_proportions, header=0, sheet_name="Sheet1")
            apply = form.cleaned_data['apply_weights']
            custom = form.cleaned_data['custom_weights']
            if custom:
                if len(formset) < 1:
                    return HttpResponse(
                        "Error: Please specify your custom weights in the form."
                        )
                groups = []
                questions = []
                for sub_form in formset:
                    groups.append(sub_form.cleanded_data['group'])
                    questions.append(sub_form.cleanded_data['question'])

            # print(groups)
            # print(questions)

            # Run ipf module
            if apply:
                weighted_data = wgt.run_weighting(survey_data, weight_proportions)
            # elif custom:
            #     weighted_data = wgt.apply_custom_weight(survey_data, weight_proportions)
            else:
                weighted_data = wgt.apply_no_weight(survey_data)

            response = HttpResponse(
                weighted_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
            )
            response['Content-Disposition'] = 'attachment; filename="weighted_data.xlsx"'

            # Cache the weighted data to be downloaded by user later
            excel_buffer = BytesIO()
            weighted_data.to_excel(excel_buffer, index=False)
            excel_buffer.seek(0)
            unique_id = "weights_for_user_" + str(request.user.id)
            cache.set(unique_id, excel_buffer.getvalue(), 300)
            # messages.success(request, "Data successfully weighted")
            # return redirect(reverse('home'))
            response = HttpResponse(
                excel_buffer.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
            )
            response['Content-Disposition'] = 'attachment; filename="weighted_data.xlsx"'
            return response
        else:
            messages.error(request, "Invalid form submission. Please try again")
            return redirect(reverse('home'))
    else:
        form = WeightForm()
        formset = CustomWeightFormSet(prefix="weights")

    return render(request, 'weight_form.html', {
        'form': form,
        'formset': formset
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
            messages.error(request, "You cannot access this feature until you are logged in")
            return redirect(reverse('home'))
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
                    cb_answer = sub_form.cleaned_data['non_standard_cb_answers']
                    if "|" in cb_answer:
                        cb_answer = cb_answer.split("|")
                    cb_data = [cb_name, cb_question, cb_answer]
                    non_standard_cb.append(cb_data)

            # convert the data to python-readable formats
            data = pd.read_excel(data_file, header=0, sheet_name="Sheet1")
            data.columns = [preprocess_header(col) for col in data.columns]

            # validate the standard crossbreaks the the user selects.
            is_valid = vld.validate_cb_inputs(data, standard_cb)
            if not is_valid[0]:
                return HttpResponse(f"An error occured: {is_valid[1]}")

            # get question data from API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # JSON AND CSV OUTPUT CURRENTLY COMMENTED OUT FOR PERFORMANCE
            survey_questions = get_questions_json(survey_id)
            if survey_questions is None:
                message = """
                    No data returned from Alchemer.
                    Did you enter a valid surveyID?
                    """
                return HttpResponse(message)
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
            # messages.success(request, "Crossbreaks successfully calculated!")
            # Redirect user to homepage.
            # return redirect(reverse('home'))

            response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="crossbreaks_data.csv"'
            return response
        else:
            messages.error(
                request,
                "There was a problem processing this request. Please try again."
            )
            return redirect('home')
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
        response['Content-Disposition'] = 'attachment; filename="crossbreaks_data.csv"'
        return response
    else:
        messages.error(
            request,
            "No crossbreaks data found. Please run the calculations first."
        )
        return redirect('home')

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
        messages.error(
            request,
            "No weighted data found. Please weight the data first."
        )
        return redirect('home')

def preprocess_header(header):
    """
    Helper func to normalise encoding:
    1. remove any chars that look like
    space but aren't.
    2. replace weird hyphens with normal
    hyphens.
    """
    header = header.encode('utf-8').decode('utf-8')
    header = re.sub(r'\s+', ' ', header)
    en_dash = '\u2013'
    hyphen_minus = '\u002D'
    header.replace(en_dash, hyphen_minus)
    return header
