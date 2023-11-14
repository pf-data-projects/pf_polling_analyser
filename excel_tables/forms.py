from django import forms
from django.forms import formset_factory

class TableUploadForm(forms.Form):
    """
    A class to handle the upload of the calculated table so
    that it can be scanned to prompt user
    """

    data_file = forms.FileField(
        label='UPLOAD THE TABLE HERE',
        help_text='Only .xlsx files are accepted.',
        validators=[]
    )
    title = forms.CharField(
        label="Title you want to give to the survey",
        required=True,
    )
    start = forms.IntegerField(
        label="Select which question ID you would like the table to start at",
        help_text="For now, you need to specify the question ID here. It's the number that the question has in the results sheet you download from Alchemer.",
        required=True
    )
    end = forms.IntegerField(
        label="Select which question ID you would like the table to end at",
        required=True
    )
