"""
This file wil take the crossbreak data from the view and
process it into a list of dictionaries that contain the following
information about each crossbreak:
1. column name
2. question needed to isolate the desired values.
3. Answer to this question with which to filter results.
"""

from . import helpers
from . import calc
from .rebase import rebase


def calc_crossbreak(table, question_list, results, question_data, crossbreak):
    """
    This function filters the results for the crossbreak
    and runs the calculation loop.
    """
    crossbreak_q = crossbreak[1]
    for answer in crossbreak[2]:
        col_index = table.columns.get_loc(f'{crossbreak[0]}: {answer}')
        for question in question_list:
            get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
            print(get_crossbreak)
            filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
            table.iat[0, col_index] = len(filtered_df.index)
            table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()
            table = calc.calc(filtered_df, col_index, table, question, results, question_data, False)
    return table


def rebase_crossbreak(table, question_list, results, question_data, crossbreak):
    """
    Passes data to run the rebase code for any
    non standard crossbreak.
    """
    crossbreak_q = crossbreak[1]
    for answer in crossbreak[2]:
        col_index = table.columns.get_loc(f'{crossbreak[0]}: {answer}')
        get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
        filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
        table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table
