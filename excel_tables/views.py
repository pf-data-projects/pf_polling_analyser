from io import BytesIO

import pandas as pd

from django.shortcuts import render, reverse, redirect
from django.core.cache import cache
from django.http import HttpResponse

from .forms import TableUploadForm
from .table_maker.trim import trim_table
from .table_maker.workbook import create_workbook

def table_maker_form(request):
    """
    A view that:
    1. calls the run_weighting function in the weight file.
    """
    if request.method == 'POST':
        form = TableUploadForm(request.POST, request.FILES)
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

    return render(request, 'table_maker_form.html', {
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
