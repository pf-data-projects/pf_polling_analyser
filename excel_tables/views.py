from io import BytesIO

import pandas as pd

from django.shortcuts import render, reverse, redirect
from django.core.cache import cache
from django.http import HttpResponse
from django.forms import formset_factory

from .forms import TableUploadForm, RebaseForm, TableScanForm
from .table_maker.trim import trim_table
from .table_maker.workbook import create_workbook

def table_maker_form(request, arg1):
    """
    A view that:
    1. calls the run_weighting function in the weight file.
    """
    rebase_questions = request.session.get('rebase_questions')
    if request.method == 'POST':
        form = TableUploadForm(request.POST, request.FILES)
        RebaseFormSet = formset_factory(RebaseForm)
        formset = RebaseFormSet(request.POST)
        if form.is_valid():
            # Fetches data from form & converts them to df
            table_data = request.FILES['data_file']
            table_data = pd.read_csv(table_data)
            title = form.cleaned_data['title']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            # Run table maker modules
            trimmed = trim_table(table_data, start, end)

            # create and cache excel tables.
            create_workbook(request, trimmed, title)

            print("table making SUCCESS!!")
            return redirect(reverse('home'))
    else:
        form = TableUploadForm()
        print(len(rebase_questions))
        RebaseFormSet = formset_factory(RebaseForm, extra=0)
        my_list = [1, 2, 3, 4, 5]

        formset = RebaseFormSet(initial=[{'item_number': number} for number in rebase_questions])

    return render(request, 'table_maker_form.html', {
        'form': form,
        'formset': formset,
        'questions': rebase_questions
    })

def scan_table(request):
    """
    Handles the logic to scan and find which questions
    need a new rebase comment.
    """
    if request.method == 'POST':
        form = TableScanForm(request.POST, request.FILES)
        if form.is_valid():
            # Fetches data from form & converts them to df
            table_data = request.FILES['data_file']
            table_data = pd.read_csv(table_data)
            filtered_df = table_data[
                (table_data['Base Type'] == 'Question') & (table_data['Rebase comment needed'] == 'TRUE')
            ]

            filtered_df.set_index('IDs', inplace=True)
            id_answer_dict = filtered_df['Answers'].to_dict()

            forms_needed = len(id_answer_dict)

            rebase_questions = []
            for key, value in id_answer_dict.items():
                pair = f"{key}: {value}"
                rebase_questions.append(pair)

            request.session['rebase_questions'] = rebase_questions

            return redirect('table_maker', arg1=forms_needed)
    else:
        form = TableScanForm()

    return render(request, 'table_scan_form.html', {
        'form': form,
    })

def download_tables(request):
    """
    Handles retrieval of cached weighted data.
    """
    unique_id = "tables_for_user_" + str(request.user.id)
    excel_data = cache.get(unique_id)
    if excel_data:
        response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="download.xlsx"'
        return response
    else:
        return HttpResponse("TABLES NOT FOUND")
