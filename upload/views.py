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

def read_word_file(file):
    """ 
    Helper function to convert word file into string.
    """
    doc = Document(file)
    result = []
    for paragraph in doc.paragraphs:
        result.append(paragraph.text)
    return '\n'.join(result)

def weight_data(request):
    """
    A view that:
    1. calls the run_weighting function in the weight file.
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
    1. renders the csv upload form
    2. reads submitted csvs as a pandas dataframe
    """
    if request.method == 'POST':
        if not request.user.is_authenticated:
            print('You are not logged in to the PF polling analyser.')
            print('You cannot make this request until you log in.')
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
                    cb_answer = sub_form.cleaned_data['non_standard_cb_answer']
                    cb_data = [cb_name, cb_question, cb_answer]
                    non_standard_cb.append(cb_data)

            # convert the data to python-readable formats
            data = pd.read_excel(data_file, header=0, sheet_name="Sheet1")

            # get question data from API
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
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="weighted_data.xlsx"'
        return response
    else:
        return HttpResponse("WEIGHTS NOT FOUND")
