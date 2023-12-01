from django import forms


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
    dates = forms.CharField(
        label='Please specify the dates in which this survey was in the field.',
        help_text='e.g. "1st - 7th January 2000"',
        required=True
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


class RebaseForm(forms.Form):
    """
    A component for a single rebase comment in the form.
    """
    question_id = forms.IntegerField(
        label="Type the question ID here.",
        required=False
    )
    rebase = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'All respondents'}
        ),
        required=False
    )
    def __init__(self, *args, **kwargs):
        """
        Override default init func
        to create unique labels for each
        rebase comment field.
        """
        item_number = kwargs.pop('item_number', None)
        super(RebaseForm, self).__init__(*args, **kwargs)

        if item_number is not None:
            self.fields['name'].label = 'base'


class TableScanForm(forms.Form):
    """
    A class that takes just the table and scans it to find
    all the records that have a base type of 'question'
    and a TRUE rebase comment value.
    """
    data_file = forms.FileField(
        label='Upload the results',
        help_text="You will then be prompted to enter rebase comments for the questions that need it.",
        required=True
    )
