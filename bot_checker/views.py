import pandas as pd

from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import BotCheckForm



def upload_bots(request):
    """
    A function to handle uploading data
    and passing it to bot checking algorithm.
    """
    if request.method == 'POST':
        # handle unauth users
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this feature")
            return redirect(reverse('home'))
        form = BotCheckForm(request.POST, request.FILES)
        if form.is_valid():
            survey_data = request.FILES['data_file']
            survey_id = form.cleaned_data['survey_id']
            data = pd.read_excel(survey_data, header=0, sheet_name="Sheet1")
            

