"""
A module to handle submitting bug reports
to the database.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Django
from django.shortcuts import redirect
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .models import ReportMessage
from .forms import ReportForm


class CreateReportMessage(generic.CreateView, SuccessMessageMixin):
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
            messages.success(request, 'Issue report successfully submitted')
            return redirect('home')
        else:
            form = ReportMessage()
            print("Issue report submission not valid. Please try again.")
            messages.error(
                request,
                "Issue report submission not valid. Please try again."
            )
            return redirect('report')
