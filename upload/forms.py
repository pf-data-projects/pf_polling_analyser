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
    non_standard_cb_name = forms.CharField(
        label="Name of Crossbreak",
        help_text="Name you want to give this column in the table, i.e voted leave EU",
        required=False
    )
    non_standard_cb_question = forms.CharField(
        label="Question text",
        help_text="Please put the exact text of the question that determines this crossbreak here.",
        required=False
    )
    non_standard_cb_answer = forms.CharField(
        label="Answer",
        help_text="Please put the exact answer for this question which you would like to check.",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        self.fields['standard_cb'].initial = [choice[0] for choice in CB_OPTIONS]
