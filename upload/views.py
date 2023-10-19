from io import BytesIO
import json

import pandas as pd
from docx import Document

from django.shortcuts import render, redirect, reverse
from .forms import CSVUploadForm
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
    print("Running IPF on dataset")
    wgt.run_weighting()
    return redirect(reverse('home'))

def upload_csv(request):
    """
    A view that:
    1. renders the csv upload form
    2. reads submitted csvs as a pandas dataframe
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = request.FILES['data_file']
            survey_id = form.cleaned_data['survey_id']
            standard_cb = form.cleaned_data['standard_cb']
            cb_name = form.cleaned_data['non_standard_cb_name']
            cb_question = form.cleaned_data['non_standard_cb_question']
            cb_answer = form.cleaned_data['non_standard_cb_answer']
            cb_data = [cb_name, cb_question, cb_answer]

            # convert the data to python-readable formats
            data = pd.read_excel(data_file, header=0, sheet_name="Worksheet")

            # get question data from API
            survey_questions = get_questions_json(survey_id)
            questions = extract_questions_from_pages(survey_questions)
            with open("questions_list.json", "w") as outfile:
                json.dump(survey_questions, outfile, indent=2)
            question_data = extract_data_from_question_objects(questions)
            question_data.to_csv(
                "question_data.csv", index=False, encoding="utf-8-sig")

            # Run calculations
            table = table_calculation(data, question_data, standard_cb, cb_data)

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

    return render(request, 'upload_form.html', {
        'form': form,
    })
