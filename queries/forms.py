from django import forms
from .models import Query


class QueryForm(forms.ModelForm):
    """
    A class to display functioning form for Query model.
    """
    class Meta:
        model = Query
        fields = ('survey_name', 'starting_qid', 'ending_qid')
        labels = {
            'survey_name': 'Exact name as it appears in Alchemer',
            'starting_qid': 'Starting Question ID',
            'ending_qid': 'Ending Question ID'
        }
