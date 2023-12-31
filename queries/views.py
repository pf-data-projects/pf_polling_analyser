"""
Views to handle the CRUD functionality for db queries.

Also contains a view to make a query to the alchemer API
using data specified by the user.
"""

# ~~~~~~~~  Imports ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Django
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic, View

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal

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
