from django import forms

CB_OPTIONS = (
        ('gender', 'Gender'),
        ('age', 'Age'),
        ('region', 'Region'),
    )

class CSVUploadForm(forms.Form):
    """
    A class to handle the upload of:
    1. survey results spreadsheet.
    2. the alchemer id of the survey
    3. any future inputs, such as crossbreaks, other data etc.
    """

    data_file = forms.FileField(
        label='SURVEY RESPONSE DATA ONLY',
        help_text='Only .xlsx files are accepted.',
        validators=[]
    )
    survey_id = forms.IntegerField(
        label='SURVEY ID',
        help_text='This can be found on the first page of the survey legend',
        required=True
        )
    standard_cb = forms.MultipleChoiceField(
        choices=CB_OPTIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        self.fields['standard_cb'].initial = [choice[0] for choice in CB_OPTIONS]
