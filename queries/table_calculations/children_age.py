"""
Handles unique logic for the columns in the data
that deal with the qestion asking respondents if they
have children and if so how old they are.
"""

from . import helpers
from . import calc
from .rebase import rebase

AGE_QUESTIONS = [
    "No children",
    "Yes - child/children aged under 5 years old",
    "Yes - child/children aged 5-10 years old",
    "Yes - child/children aged 11-15 years old",
    "Yes - child/children aged 16-18 years old",
    "Yes - child/children over 18 years old",
]

def iterate_over_children_ages(table, question_list, results, question_data):
    """
    Iterates over the different column
    options for this crossbreak to calculate responses.
    """
    table_col = table.columns.get_loc('No children')
    for question_header in AGE_QUESTIONS:
        try:
            get_col = results[helpers.col_substr_partial(results, question_header)]
            # print(get_col)
            filtered_df = results.loc[results[get_col.columns[0]] != 'nan']
            table.iat[0, table_col] = len(filtered_df.index)
            # print(len(filtered_df.index))
            table.iat[1, table_col] = filtered_df['weighted_respondents'].astype(float).sum()
            for question in question_list:
                table = calc.calc(
                    filtered_df, table_col, table, question, results, question_data, False)
            table_col += 1
        except IndexError:
            print("there was an encoding error.")
            continue
    return table

def rebase_children_ages(table, question_list, results, question_data):
    """
    Iterates over the different column
    options for this crossbreak to rebase responses.
    """
    table_col = table.columns.get_loc('No children')
    for question_header in AGE_QUESTIONS:
        get_col = results[helpers.col_substr_partial(results, question_header)]
        filtered_df = results.loc[results[get_col.columns[0]].notna()]
        table = rebase(question_data, filtered_df, question_list, table, table_col)
        table_col += 1
    return table
