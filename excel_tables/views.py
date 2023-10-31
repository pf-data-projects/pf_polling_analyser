import BytesIO

import pandas as pd

from django.shortcuts import render, reverse, redirect
from .forms import TableUploadForm
from django.core.cache import cache
from django.http import HttpResponse

def table_maker_form(request):
    """
    A view that:
    1. calls the run_weighting function in the weight file.
    """
    if request.method == 'POST':
        form = TableUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Fetches data from form & converts them to df
            # survey_data = request.FILES['results']
            # survey_data = pd.read_excel(survey_data, header=0, sheet_name="Worksheet")
            # weight_proportions = request.FILES['weights']
            # weight_proportions = pd.read_excel(weight_proportions, header=0, sheet_name="Sheet1")

            # Run table maker module

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
