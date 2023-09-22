# ~~~~~~~~  Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
from time import sleep

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Django
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Other 3rd party
import pandas as pd

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .api_request.get_survey_metadata import get_all_pages_of_surveys
from .api_request.get_survey_id import get_survey_id
from .api_request.get_survey_questions import get_questions_json
from .api_request.get_processed_questions import (
    extract_data_from_question_objects,
    extract_questions_from_pages
)
from .api_request.get_survey_responses import get_responses

from .table_calculations.calculate_totals import table_calculation

from .forms import QueryForm
from .models import Query


class QueryList(generic.ListView):
    """
    A class to display list of Query objects.
    """
    model = Query
    queryset = Query.objects.all()
    template_name = 'query_list.html'
    paginate_by = 10


class QueryCreate(generic.CreateView):
    """
    A class to create Query objects and save to db.
    """
    model = Query
    form_class = QueryForm
    template_name = 'query_form.html'

    def form_valid(self, form):
        """
        A function to validate form and save to db.
        """
        form.instance.user = self.request.user
        super().form_valid(form)
        return redirect(reverse('home'))


class QueryDetail(View):
    """
    A class to display Query object details.
    """
    def get(self, request, pk):
        """
        A method to display Query object details.
        """
        queries = Query.objects.all()
        query = get_object_or_404(queries, pk=pk)
        return render(request, 'query_detail.html', {'query': query})

# WARNING: This view is asynchronous and needs time to execute.
def make_request(request, pk):
    """
    A function to make a request to alchemer api.
    """
    if not request.user.is_authenticated:
        print('you are not authorised to make this request.')
        return redirect(reverse('home'))

    # get all survey metadata to find the survey id for the user.
    print('making request to the api...')
    query = get_object_or_404(Query, pk=pk)
    survey_list = get_all_pages_of_surveys()
    survey_id = get_survey_id(survey_list, query.survey_name)
    # manually throttle app to prevent from exceeding 240/min limit.
    print(survey_id)
    for i in range(0, 60):
        print(f'Manual throttle: waiting {60 - i} seconds...')
        sleep(1)

    # get all questions of survey from db, unpaginate, return relevant data.
    survey_questions = get_questions_json(survey_id)
    questions = extract_questions_from_pages(survey_questions)
    question_data = extract_data_from_question_objects(questions)

    # get all responses to the survey in dataframe format.
    response_data = get_responses(survey_id)
    # print(response_data)

    # process the data
    table = table_calculation(response_data, question_data)


    return redirect(reverse('home'))
