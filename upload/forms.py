from django import forms

class CSVUploadForm(forms.Form):
    """
    A class to handle the upload of:
    1. survey results spreadsheet.
    2. order spreadsheet.
    3. survey legend.
    """
    data_file = forms.FileField(
        label='SURVEY RESPONSE DATA ONLY',
        help_text='Only .xlsx files are accepted.',
        validators=[]
    )
    order_file = forms.FileField(
        label='SURVEY ORDER ONLY',
        help_text='Only .xlsx files are accepted.',
        validators=[]
    )
    survey_legend_file = forms.FileField(
        label='SURVEY LEGEND ONLY',
        help_text='Only .docx files are accepted.',
        validators=[]
    )
