"""
This file defines the forms for the weighting section of the code
as well as the crossbreak form calculator. The forms include:

1. CSVUploadForm: the overall form for handling the upload 
of the weighted data along with standard crossbreaks.

2. CrossbreakFormSet: the formset to handle sub-forms for
individual non-standard crossbreaks. This uses Django's built-in 
formset_factory function.

3. CrossbreakForm: the fields for the individual forms
for the non-standard crossbreaks.

4. WeightForm: the form that handles the upload of unweighted
data, weight propotions, and whether the user would like to
weight the data.
"""

from django import forms
from django.forms import formset_factory

CB_OPTIONS = (
    ('gender', 'Gender'),
    ('age', 'Age'),
    ('region', 'Region'),
    ('seg', 'Socio-economic Grade'),
    ('children', 'Children'),
    ('children(updated)', "Children (Age breakdown)"),
    ('education', 'Education'),
    ('income', 'Income'),
    ('area', 'Area'),
    ('vote2019', 'Vote 2019'),
    ('eu2016', 'EU 2016 Vote'),
    ('voting_intention', 'Voting Intention')
)

STANDARD_WEIGHTS = (
    ('seg', 'Socio-economic Grade'),
    ('region', 'Region'),
    ('genderage', 'Interlocking Gender and Age')
)


class CSVUploadForm(forms.Form):
    """
    A class to handle the upload of:
    1. survey results spreadsheet.
    2. the alchemer id of the survey
    3. any future inputs, such as crossbreaks, other data etc.
    """

    data_file = forms.FileField(
        label='Survey Response Data (weighted_data.xlsx)',
        validators=[]
    )
    survey_id = forms.IntegerField(
        label='Survey ID',
        help_text='This can be found on the first page of the survey legend',
        required=True
    )
    standard_cb = forms.MultipleChoiceField(
        label="Select which standard crossbreaks to include",
        choices=CB_OPTIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CSVUploadForm, self).__init__(*args, **kwargs)
        self.fields['standard_cb'].initial = [choice[0] for choice in CB_OPTIONS]


class CrossbreakForm(forms.Form):
    """
    Constitutes the main element of formset to
    handle multiple new crossbreak entries.
    """
    non_standard_cb_name = forms.CharField(
        label="Name of Crossbreak",
        help_text="Name you want to give this column in the table, i.e voted leave EU",
        required=False
    )
    non_standard_cb_question = forms.CharField(
        label="Question text",
        help_text="""
            Please put the exact text of the question
            that determines this crossbreak here
            (and don't include the question id number).
            """,
        required=False
    )
    non_standard_cb_answers = forms.CharField(
        label="Answers",
        help_text="""
        Enter the answers for this question which you would like to check,
        separated by | e.g., Yes|No|Maybe
        """,
        required=False
    )

CrossbreakFormSet = formset_factory(CrossbreakForm, extra=1)


class WeightForm(forms.Form):
    """
    A form to handle the uploading of:
    1. polling data
    2. weight proportions
    """
    results = forms.FileField(
        label='Survey Response Data (same data file you would use normally)',
        validators=[]
    )
    weights = forms.FileField(
        label='Weight Proportions Data',
        validators=[],
        required=False
    )
    apply_weights = forms.BooleanField(
        label="Weight the data with standard weighting:",
        required=False
    )
    custom_weights = forms.BooleanField(
        label="Customise your weights:",
        help_text="Don't check this unless you're using custom weights",
        required=False
    )
    standard_weights = forms.MultipleChoiceField(
        label="""
        Do you want to include any standard weights 
        in the custom weighting process?
        """,
        choices=STANDARD_WEIGHTS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


class CustomWeightForm(forms.Form):
    """
    A form to handle custom fields by which
    the data will be weighted by the program.
    """
    group = forms.CharField(
        label="""
        The category you want to weight by: e.g., 
        Region, Ethnicity, Income, etc...
        """,
        help_text="""
        This needs to match the custom category in the 
        'group' column of the weight proportions file
        """,
        required=False
    )
    question = forms.CharField(
        label="The exact question in the survey associated with this category",
        required=False
    )

CustomWeightFormSet = formset_factory(CustomWeightForm, extra=1)
