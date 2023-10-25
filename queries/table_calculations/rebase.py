import pandas as pd
from . import helpers

def rebase(results, question_list, table):
    """
    1. Checks each col of results and if there are any NaN values
    2. Runs the rebasing code if so,
    3. Passes if not.
    4. returns updated table.
    """
    weighted_totals = table.iloc[1, 5]
    print(weighted_totals)
    checked = []
    for question in question_list:
        column = results[helpers.col_with_substr_a(results, question['question'], question['qid'])]
        contains_nan = (column == 'nan').any().any()
        if column.empty:
            continue
        elif contains_nan:
            print("-----------------------")
            print(question['qid'])
            non_nan_count = column[column != 'nan'].count().iloc[0]
            # Get indices of rows in 'table' that match question['qid']
            matching_indices = table[table['IDs'] == question['qid']].index
            if question['qid'] not in checked:
                # Reverse the percentage calculation for these rows
                for idx in matching_indices:
                    percentage_value = table.iloc[idx, 5]
                    table.iloc[idx, 5] = (percentage_value / 100) * weighted_totals
                    print(non_nan_count)
                    print(table.iloc[idx, 5])
                    
                    # Then, update the values in these rows to be their percentage of non_nan_count
                    value = table.iloc[idx, 5]
                    table.iloc[idx, 5] = (value / non_nan_count) * 100
                    
            checked.append(question['qid'])
        else:
            continue
    # return table
