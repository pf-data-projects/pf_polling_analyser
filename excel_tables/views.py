from io import BytesIO

import pandas as pd

from django.shortcuts import render, reverse, redirect
from django.core.cache import cache
from django.http import HttpResponse

from .forms import TableUploadForm
from .table_maker.trim import trim_table

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
            print(trimmed.head(10))
            print(trimmed.tail(10))

            # Cache the tables to be downloaded by user later
            # excel_buffer = BytesIO()
            # weighted_data.to_excel(excel_buffer, index=False)
            # excel_buffer.seek(0)
            # unique_id = "tables_for_user_" + str(request.user.id)
            # cache.set(unique_id, excel_buffer.getvalue(), 300)
            print("table making SUCCESS!!")
            return redirect(reverse('home'))
    else:
        form = TableUploadForm()

    return render(request, 'table_maker_form.html', {
        'form': form,
    })
