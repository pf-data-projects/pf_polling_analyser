import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc
from .rebase import rebase

def calc_gender(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    gender_q = 'Which of the following best describes how you think of yourself?'
    for question in question_list:
        get_gender = results[helpers.col_with_substr_q(results, gender_q)]
        filtered_df = results.loc[(results[get_gender.columns[0]] == category)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()

        table = calc.calc(filtered_df, col_index, table, question, results, question_data)

    # print(category, "done!")
    return table

def gender_rebase(category, col_index, table, question_list, results, question_data):
    """
    Filters the results and then passes
    relevant data to rebase function.
    """
    gender_q = 'Which of the following best describes how you think of yourself?'
    get_gender = results[helpers.col_with_substr_q(results, gender_q)]
    filtered_df = results.loc[(results[get_gender.columns[0]] == category)]

    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table
