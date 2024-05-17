"""
This file contains the form class used to collect survey data
and IDs to be used by the bot-checking algorithm.

BotCheckForm
"""

from django import forms


class BotCheckForm(forms.Form):
    """
    A class to handle the upload of:
    1. survey data to be checked
    2. the survey id so that questions can be checked.
    """
    CHOICES = (
        ('is_word', 'Check for real words'),
        ('sense', 'Check if answer makes sense (Uses OpenAI API)'),
        ('duplicate', 'Check for duplicates'),
    )
    data_file = forms.FileField(
        label="Raw survey data (.xlsx file)",
        validators=[]
    )
    survey_id = forms.IntegerField(
        label="Survey ID",
        help_text='This can be found on the first page of the survey legend',
        required=True
    )
    check = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.RadioSelect(),
        label="Select which check you'd like to carry out"
    )
