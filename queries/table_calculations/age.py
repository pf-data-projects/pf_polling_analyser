import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc
from .rebase import rebase

def calc_age(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    age_q = 'How old are you?'
    for question in question_list:
        get_age = results[helpers.col_with_substr_q(results, age_q)].astype(int)
        filtered_df = results.loc[
            (results[get_age.columns[0]].astype(int) >= category[0])
            ]
        filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(int) <= category[1])]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()
        table = calc.calc(filtered_df, col_index, table, question, results, question_data)

    print(category[0], "done!")
    return table

def age_rebase(category, col_index, table, question_list, results, question_data):
    """
    Filters the results and then passes
    relevant data to rebase function.
    """
    age_q = 'How old are you?'
    get_age = results[helpers.col_with_substr_q(results, age_q)].astype(int)
    filtered_df = results.loc[
        (results[get_age.columns[0]].astype(int) >= category[0])
        ]
    filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(int) <= category[1])]

    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table

def iterate_age_brackets(table, question_list, results, question_data):
    """ 
    Builds a list of age brackets
    and calls the calc_age func based on the data
    in the list of age bracket objects.
    """
    ages = cb.CROSSBREAKS["age"]
    table_col = table.columns.get_loc("18-24")
    age_brackets = []
    for age in ages:
        if "-" in age:
            num1 = int(age.split("-", 1)[0])
            num2 = int(age.split("-", 1)[1])
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        else:
            num1 = int(age.split("+", 1)[0])
            num2 = 200
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        table_col += 1
    for bracket in age_brackets:
        table = calc_age(
            [bracket['num1'], bracket['num2']],
            bracket['col'],
            table,
            question_list,
            results,
            question_data
        )
    return table

def iterate_age_rebase(table, question_list, results, question_data):
    """ 
    Builds a list of age brackets from the cb module
    and calls the calc_age func based on the data
    in the list of age bracket objects.
    """
    ages = cb.CROSSBREAKS["age"]
    table_col = table.columns.get_loc("18-24")
    age_brackets = []
    for age in ages:
        if "-" in age:
            num1 = int(age.split("-", 1)[0])
            num2 = int(age.split("-", 1)[1])
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        else:
            num1 = int(age.split("+", 1)[0])
            num2 = 200
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        table_col += 1
    for bracket in age_brackets:
        table = age_rebase(
            [bracket['num1'], bracket['num2']],
            bracket['col'],
            table,
            question_list,
            results,
            question_data
        )
    return table
