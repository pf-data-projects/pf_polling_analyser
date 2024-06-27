import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc
from .rebase import rebase

SEG_MAPPING = {
        'AB': [
            "Higher managerial/ professional/ administrative (e.g. Established doctor, Solicitor, Board Director in a large organisation (200+ employees, top level civil servant/public service employee))",
            "Intermediate managerial/ professional/ administrative (e.g. Newly qualified (under 3 years) doctor, Solicitor, Board director small organisation, middle manager in large organisation, principle officer in civil service/local government)",
        ],
        'C1': [
           "Student",
           "Supervisory or clerical/junior managerial/professional/administrative (e.g. Office worker, Student Doctor, Foreman with 25+ employees, salesperson, etc.)", 
        ],
        'C2': [
            "Skilled manual worker (e.g. Skilled Bricklayer, Carpenter, Plumber, Painter, Bus/ Ambulance Driver, HGV driver, AA patrolman, pub/bar worker, etc.)",
        ],
        'DE': [
            "Casual worker - not in permanent employment",
            "Full-time carer of other household member",
            "Housewife/Househusband/Homemaker",
            "Retired and living on state pension",
            "Semi or unskilled manual work (e.g. Manual workers, all apprentices to be skilled trades, Caretaker, Park keeper, non-HGV driver, shop assistant)",
            "Unemployed or not working due to long-term sickness"
        ],
    }

def calc_seg(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """

    seg_q = 'Think about the Chief Income Earner in your household'
    for question in question_list:
        get_seg = results[helpers.col_substr_partial(results, seg_q)]
        contains = get_seg.iloc[:, 0].isin(category)
        filtered_df = results[contains]
        # filtered_df = results.loc[(results[get_seg.columns[0]] == category)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()

        table = calc.calc(filtered_df, col_index, table, question, results, question_data, False)

    # print(category, "done!")
    return table

def seg_rebase(category, col_index, table, question_list, results, question_data):
    """
    Filters the results and then passes
    relevant data to rebase function.
    """
    seg_q = 'Think about the Chief Income Earner in your household'
    get_seg = results[helpers.col_substr_partial(results, seg_q)]
    contains = get_seg.iloc[:, 0].isin(category)
    filtered_df = results[contains]

    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table

def iterate_seg(table, question_list, results, question_data):
    """
    Loops through the list of regions and
    builds a list of dictionaries which
    contain the necessary arguments for a call
    of the calc_region function.
    """
    segs = cb.CROSSBREAKS['seg']
    table_col = table.columns.get_loc('AB')
    seg_iterator = []
    for seg in segs:
        iteration = {
            'seg': SEG_MAPPING[seg],
            'col': table_col
        }
        seg_iterator.append(iteration)
        table_col += 1
    for iteration in seg_iterator:
        table = calc_seg(
            iteration['seg'],
            iteration['col'], table, question_list, results, question_data
            )
    return table

def iterate_seg_rebase(table, question_list, results, question_data):
    """
    Loops through the list of regions and
    builds a list of dictionaries which
    contain the necessary arguments for a call
    of the region_rebase function.
    """
    segs = cb.CROSSBREAKS['seg']
    table_col = table.columns.get_loc('AB')
    seg_iterator = []
    for seg in segs:
        iteration = {
            'seg': SEG_MAPPING[seg],
            'col': table_col
        }
        seg_iterator.append(iteration)
        table_col += 1
    for iteration in seg_iterator:
        table = seg_rebase(
            iteration['seg'],
            iteration['col'], table, question_list, results, question_data
            )
    return table
