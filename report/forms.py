"""
This module contains all the classes for
defining form structures for the report app.
"""

from django import forms
from .models import ReportMessage


class ReportForm(forms.ModelForm):
    """
    A class for generating form fields needed to
    submit report data to the db.
    """
    class Meta:
        model = ReportMessage
        fields = ('message',)
        labels = {'message': 'Please specify the problem you are having'}
