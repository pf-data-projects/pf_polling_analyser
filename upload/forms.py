from django import forms

class CSVUploadForm(forms.Form):
    """
    A class to handle the upload of:
    1. survey results csvs.
    2. order csvs.
    3. survey legend.
    """
    csv_file = forms.FileField(
        label='Upload a CSV file',
        help_text='Only .csv files are accepted.',
        validators=[]
    )
