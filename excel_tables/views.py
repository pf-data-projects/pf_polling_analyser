"""
These views handle the page logic for all pages associated
with the excel_tables app.

1. scan_table either returns empty form, or finds out how many
forms are required for the rebase comment section of the main
table form and saves them in session storage (in the DB I think...).

2. table_maker_form returns a blank form (with appropriate number of
rebase comment forms) when the user scans their dataset. Or, it will
handle the logic for creating a set of polling tables.

~~ Currently this is a little awkward as the user must upload 
their data twice. Maybe we could cache it, but don't
want to waste memory ~~

3. download_tables works like other download functions. It fetches 
and downloads tables from the cache if they exist and displays an
error if not.
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
import json

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
import pandas as pd

from django.shortcuts import render, redirect
from django.core.cache import cache
from django.http import HttpResponse
from django.forms import formset_factory
from django.contrib import messages

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from .forms import TableUploadForm, RebaseForm, TableScanForm
from .table_maker.trim import trim_table
from .table_maker.workbook import create_workbook


def table_maker_form(request, arg1):
    """
    A view that:
    1. calls the run_weighting function in the weight file.
    """
    unique_id = "rebase_questions_for_user_" + str(request.user.id)
    rebase_questions = cache.get(unique_id)
    if request.method == 'POST':
        form = TableUploadForm(request.POST, request.FILES)
        RebaseFormSet = formset_factory(RebaseForm)
        formset = RebaseFormSet(request.POST)
        if not form.is_valid():
            cache.set("test", form.errors, 300)
        if form.is_valid() and formset.is_valid():
            # ~~~~~~~~~~~~~~~~~~~ Fetches data from form & converts them to df
            table_data = request.FILES['data_file']
            table_data = pd.read_csv(table_data)
            rebased_headers = request.FILES['rebased_header_file']
            rebased_headers = json.load(rebased_headers)
            title = form.cleaned_data['title']
            dates = form.cleaned_data['dates']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            id_column = form.cleaned_data['id_column']
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fetches data from formset
            edited_comments = []
            j = 0
            for sub_form in formset:
                comment = sub_form.cleaned_data['rebase']
                question = rebase_questions[1][j]
                comment_data = [question, comment]
                if question is None or comment == "":
                    continue
                else:
                    edited_comments.append(comment_data)
                j += 1
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Run table maker modules
            trimmed = trim_table(table_data, start, end, edited_comments)
            if trimmed is False:
                return HttpResponse(
                    "Invalid start or end ID."
                )
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create and cache excel tables
            cache_key = create_workbook(
                request, trimmed[0], trimmed[1], trimmed[2], trimmed[3],
                title, dates, edited_comments, start, end, 
                id_column, rebased_headers
            )
            unique_id = "title_for_user_" + str(request.user.id)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ auto-download for the excel tables
            excel_data = cache.get(cache_key)
            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{title}.xlsx"'
            return response
        else:
            messages.error(
                request,
                "Invalid form data was submitted. please try again"
            )
            return redirect('home')
    else:
        form = TableUploadForm()
        RebaseFormSet = formset_factory(RebaseForm, extra=0)
        formset = RebaseFormSet(initial=[{'item_number': number} for number in rebase_questions[0]])

    return render(request, 'table_maker_form.html', {
        'form': form,
        'formset': formset,
        'questions': rebase_questions[0]
    })


def scan_table(request):
    """
    Handles the logic to scan and find which questions
    need a new rebase comment.
    """
    if request.method == 'POST':
        form = TableScanForm(request.POST, request.FILES)
        if form.is_valid():
            # ~~~~~~~~~~~~~~~~~~~ Fetches data from form & converts them to df
            table_data = request.FILES['data_file']
            table_data = pd.read_csv(table_data, encoding="utf-8-sig")
            # ~~~ Filters df to get only questions that have true rebase value
            filtered_df = table_data[
                (table_data['Base Type'] == 'Question')
            ]
            filtered_df = filtered_df[filtered_df['Rebase comment needed'].isin(['TRUE', 'True'])]
            filtered_df.set_index('IDs', inplace=True)

            # ~~~~~~~~~~~~~~~~ remove html tags from questions for rebase form
            filtered_df["Answers"] = filtered_df["Answers"].str.replace(
                r'<[^>]+>', '', regex=True
            )
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Add these questions to a dictionary
            id_answer_dict = filtered_df['Answers'].to_dict()
            forms_needed = len(id_answer_dict)
            rebase_questions = []
            for key, value in id_answer_dict.items():
                pair = f"{key}: {value}"
                rebase_questions.append(pair)
            rebase_ids = [key for key, value in id_answer_dict.items()]

            rebase_questions = [rebase_questions, rebase_ids]
            unique_id = "rebase_questions_for_user_" + str(request.user.id)
            cache.set(unique_id, rebase_questions, 3600)

            messages.success(
                request,
                "Crossbreaks successfully scanned."
            )
            return redirect('table_maker', arg1=forms_needed)
        else:
            messages.error(
                request,
                "There was a problem processing this form. Please try again"
            )
            return redirect('scan_table')
    else:
        form = TableScanForm()

    return render(request, 'table_scan_form.html', {
        'form': form,
    })


def download_tables(request):
    """
    Handles retrieval of cached weighted data.
    """
    unique_id = "tables_for_user_" + str(request.user.id)
    unique_title = "title_for_user_" + str(request.user.id)
    excel_data = cache.get(unique_id)
    title = cache.get(unique_title)
    if excel_data:
        response = HttpResponse(
            excel_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{title}.xlsx"'
        messages.success(request, "Downloading tables...")
        return response
    else:
        messages.error(
            request,
            "No polling tables found. Please create them first."
        )
        return redirect('home')


def download_pdf(request):
    """
    Handles retrieval of cached pdf.
    """
    unique_id = "pdf_for_user_" + str(request.user.id)
    unique_title = "title_for_user_" + str(request.user.id)
    pdf = cache.get(unique_id)
    title = cache.get(unique_title)
    if pdf:
        response = HttpResponse(pdf, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{title}.html"'
        messages.success(request, "Downloading pdf...")
        return response
    else:
        messages.error(
            request,
            "No pdf found. Please create some tables first."
        )
        return redirect('home')
