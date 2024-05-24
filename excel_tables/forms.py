"""
Defines the different forms used in the excel table generator.

1. TableUploadForm: contains all the fields for user uploading
their dataset and parameters for displaying it in tables.

2. RebaseForm: contains all the fields for an individual
rebase comment. This is handled by a formset in the view.

3. TableScanForm: This contains a single field for the user
to upload their dataset so that the backend can find out
which questions need a rebase comment form in the frontend.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
from django import forms


class TableUploadForm(forms.Form):
    """
    A class to handle the upload of the calculated table so
    that it can be scanned to prompt user
    """
    data_file = forms.FileField(
        label='Upload The Table',
        validators=[],
        required=True
    )
    rebased_header_file = forms.FileField(
        label="""
        Upload the data for the rebased headers. 
        Download this from the home page if you haven't already.
        """,
        required=True
    )
    title = forms.CharField(
        label="Title you want to give to the survey",
        required=True,
    )
    dates = forms.CharField(
        label="""
        Please specify the dates in which this 
        survey was in the field.
        """,
        required=True
    )
    start = forms.IntegerField(
        label="Select which question ID you would like the table to start at",
        required=True
    )
    end = forms.IntegerField(
        label="Select which question ID you would like the table to end at",
        required=True
    )
    id_column = forms.BooleanField(
        label="Include question IDs in contents page?",
        required=False
    )


class RebaseForm(forms.Form):
    """
    A component for a single rebase comment in the form.
    """
    rebase = forms.CharField(
        initial="Assigned Randomly",
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
        label='Upload the results (crossbreaks_data.csv)',
        required=True
    )
