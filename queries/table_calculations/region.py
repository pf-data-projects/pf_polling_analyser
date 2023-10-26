import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc
from .rebase import rebase

def calc_region(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    region_q = 'In what region of the UK do you live?'
    for question in question_list:
        get_region = results[helpers.col_with_substr_q(results, region_q)]
        filtered_df = results.loc[(results[get_region.columns[0]] == category)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()

        table = calc.calc(filtered_df, col_index, table, question, results, question_data)

    print(category, "done!")
    return table

def region_rebase(category, col_index, table, question_list, results, question_data):
    """
    Filters the results and then passes
    relevant data to rebase function.
    """
    region_q = 'In what region of the UK do you live?'
    get_region = results[helpers.col_with_substr_q(results, region_q)]
    filtered_df = results.loc[(results[get_region.columns[0]] == category)]

    table = rebase(question_data, filtered_df, question_list, table, col_index)
    print("region rebase done")
    return table

def iterate_regions(table, question_list, results, question_data):
    """
    Loops through the list of regions and
    builds a list of dictionaries which
    contain the necessary arguments for a call
    of the calc_region function.
    """
    regions = cb.CROSSBREAKS['region']
    table_col = table.columns.get_loc('London')
    regions_iterator = []
    for region in regions:
        iteration = {
            'region': region,
            'col': table_col
        }
        regions_iterator.append(iteration)
        table_col += 1
    for iteration in regions_iterator:
        table = calc_region(
            iteration['region'],
            iteration['col'], table, question_list, results, question_data
            )
    return table

def iterate_regions_rebase(table, question_list, results, question_data):
    """
    Loops through the list of regions and
    builds a list of dictionaries which
    contain the necessary arguments for a call
    of the region_rebase function.
    """
    regions = cb.CROSSBREAKS['region']
    table_col = table.columns.get_loc('London')
    regions_iterator = []
    for region in regions:
        iteration = {
            'region': region,
            'col': table_col
        }
        regions_iterator.append(iteration)
        table_col += 1
    for iteration in regions_iterator:
        table = region_rebase(
            iteration['region'],
            iteration['col'], table, question_list, results, question_data
            )
    return table
