"""
Defines the standard crossbreaks that will be used in the data analysis.
"""

from . import calc
from . import helpers
from .rebase import rebase

CROSSBREAKS = {
    "gender": ["Male", "Female"],
    "age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    "region": [
        "London", "South East", "South West", "East of England",
        "West Midlands", "East Midlands", "Yorkshire and the Humber",
        "North West", "North East", "Scotland", "Wales", "Northern Ireland"
    ],
    "seg": ['AB', 'C1', 'C2', 'DE'],
    "children": ["Yes", "No"],
    "education": [
        "GCSE or equivalent (Scottish National/O Level)",
        "A Level or equivalent (GCE/Higher/Advanced Higher)",
        "Level 4 / 5 or equivalent (HND/HNC/Higher Apprenticeship)",
        "University Undergraduate Degree (BA/BSc)",
        "University Postgraduate Degree (MA/MSc/MPhil)",
        "Doctorate (PhD/DPHil)"
    ]
}

QUESTIONS = {
    "gender": "Which of the following best describes how you think of yourself?",
    "age" : "How old are you?",
    "region": "In what region of the UK do you live?",
    "seg": "Think about the Chief Income Earner in your household",
    "children": "Do you have any children under the age of 18 living at home?",
    "education": "What is the highest level of education you have achieved?",
}

def calc_standard(value, col_index, cb_question, table, question_list, results, question_data):
    """
    A function that calls the general calc func
    for the crossbreak, col, and question supplied.
    """
    for question in question_list:
        get_cb = results[helpers.col_with_substr_q(results, cb_question)]
        filtered_df = results.loc[(results[get_cb.columns[0]] == value)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()
        table = calc.calc(filtered_df, col_index, table, question, results, question_data)
    return table

def rebase_standard(value, col_index, cb_question, table, question_list, results, question_data):
    """
    A function that calls the rebase func
    for the crossbreak, col, and question supplied.
    """
    get_gender = results[helpers.col_with_substr_q(results, cb_question)]
    filtered_df = results.loc[(results[get_gender.columns[0]] == value)]
    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table
