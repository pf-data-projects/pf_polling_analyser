import pandas as pd
from docx import Document

from django.shortcuts import render
from .forms import CSVUploadForm

from .clean_data.clean_survey_legend import clean_survey_legend
from .clean_data.clean_order import clean_order

def read_word_file(file):
    """ 
    Helper function to convert word file into string.
    """
    doc = Document(file)
    result = []
    for paragraph in doc.paragraphs:
        result.append(paragraph.text)
    return '\n'.join(result)

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
            order_file = request.FILES['order_file']
            survey_legend = request.FILES['survey_legend_file']
            # convert the data to python-readable formats
            data = pd.read_excel(data_file)
            order = pd.read_excel(order_file)
            legend_text = read_word_file(survey_legend)

            # clean_survey_legend(legend_text)
            clean_order(order)
            # print(data.head(10))
            # print(order.head(10))
            # print(legend_text)
    else:
        form = CSVUploadForm()

    return render(request, 'upload_form.html', {
        'form': form,
    })
