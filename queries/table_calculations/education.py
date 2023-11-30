import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc
from .rebase import rebase

def calc_ed(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    ed_q = 'What is the highest level of education you have achieved?'
    for question in question_list:
        get_ed = results[helpers.col_with_substr_q(results, ed_q)]
        filtered_df = results.loc[(results[get_ed.columns[0]] == category)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()

        table = calc.calc(filtered_df, col_index, table, question, results, question_data)

    print(category, "done!")
    return table

def ed_rebase(category, col_index, table, question_list, results, question_data):
    """
    Filters the results and then passes
    relevant data to rebase function.
    """
    ed_q = 'What is the highest level of education you have achieved?'
    get_ed = results[helpers.col_with_substr_q(results, ed_q)]
    filtered_df = results.loc[(results[get_ed.columns[0]] == category)]

    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table

def iterate_ed(table, question_list, results, question_data):
    """
    Loops through the different education categories and
    calls the calc_ed function for each.
    """
    education_levels = cb.CROSSBREAKS['education']
    table_col = table.columns.get_loc('GCSE or equivalent (Scottish National/O Level)')
    ed_iterator = []
    for level in education_levels:
        iteration = {
            'level': level,
            'col': table_col
        }
        ed_iterator.append(iteration)
        table_col += 1
    for iteration in ed_iterator:
        table = calc_ed(
            iteration['level'],
            iteration['col'], table, question_list, results, question_data
            )
    return table

def iterate_ed_rebase(table, question_list, results, question_data):
    """
    Loops through the different education categories and
    calls the calc_ed function for each.
    """
    education_levels = cb.CROSSBREAKS['education']
    table_col = table.columns.get_loc('GCSE or equivalent (Scottish National/O Level)')
    ed_iterator = []
    for level in education_levels:
        iteration = {
            'level': level,
            'col': table_col
        }
        ed_iterator.append(iteration)
        table_col += 1
    for iteration in ed_iterator:
        table = ed_rebase(
            iteration['level'],
            iteration['col'], table, question_list, results, question_data
            )
    return table
