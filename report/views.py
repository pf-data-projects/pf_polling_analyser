"""
A module to handle 
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Django
from django.shortcuts import render, redirect
from django.views import generic

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .models import ReportMessage
from .forms import ReportForm


class CreateReportMessage(generic.CreateView):
    """
    A class for handling submitting bug reports.
    """
    model = ReportMessage
    form_class = ReportForm
    template_name = 'report.html'

    def post(self, request, *args, **kwargs):
        """
        submits user's bug report data to db.
        """
        form = ReportForm(data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            print("Issue report successfully submitted")
            return redirect('home')
        else:
            form = ReportMessage()
            print("Issue report submission not valid")
            return redirect('report')
