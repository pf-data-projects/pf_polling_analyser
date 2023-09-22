import pandas as pd
from django.shortcuts import render
from .forms import CSVUploadForm

def upload_csv(request):
    """
    A view that:
    1. renders the csv upload form
    2. reads submitted csvs as a pandas dataframe
    """
    data = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data = pd.read_excel(csv_file)
            print(data.head(10))
    else:
        form = CSVUploadForm()

    return render(request, 'upload_form.html', {
        'form': form,
    })
