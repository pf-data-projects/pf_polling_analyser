import pandas as pd
from . import helpers

def rebase(question_data, results, question_list, table, col_index):
    """
    1. Checks each col of results and if there are any NaN values
    2. Runs the rebasing code if so,
    3. Passes if not.
    4. returns updated table.
    """
    weighted_totals = table.iloc[1, col_index]
    checked = []
    for question in question_list:
        column = results[helpers.col_with_substr_a(results, question['question'], question['qid'])]
        contains_nan = (column == 'nan').any().any()
        # if column.empty:
        #     continue
        if question['Base Type'] == 'Question' and question['type'] == 'CHECKBOX':
            checkbox_cols = results[helpers.col_with_qid(results, question['qid'])]
            has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
            if has_nan_rows:
                non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                print(question['qid'])
                print(non_nan_count)
                matching_indices = table[table['IDs'] == question['qid']].index
                for idx in matching_indices:
                    percentage_value = table.iloc[idx, col_index]
                    table.iloc[idx, col_index] = (percentage_value / 100) * weighted_totals
                    print(table.iloc[idx, col_index])
                    # Then, update the values in these rows to be their percentage of non_nan_count
                    value = table.iloc[idx, col_index]
                    table.iloc[idx, col_index] = (value / non_nan_count) * 100
                    print(table.iloc[idx, col_index])
                
        elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
            print("checkbox option")
            continue

        elif question['Base Type'] == 'Question' and question['type'] == 'TABLE':
            print("table")
        elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
            print("table option")
            continue

        elif question['Base Type'] == 'Question' and question['type'] == 'RANK':
            print("rank")
        elif question['Base Type'] == 'Option' and question['type'] == 'RANK':
            print("rank option")
            continue

        elif contains_nan and question['type'] == 'RADIO':
            non_nan_count = column[column != 'nan'].count().iloc[0]
            # Get indices of rows in 'table' that match question['qid']
            matching_indices = table[table['IDs'] == question['qid']].index
            if question['qid'] not in checked:
                # Reverse the percentage calculation for these rows
                for idx in matching_indices:
                    percentage_value = table.iloc[idx, col_index]
                    table.iloc[idx, col_index] = (percentage_value / 100) * weighted_totals
                    
                    # Then, update the values in these rows to be their percentage of non_nan_count
                    value = table.iloc[idx, col_index]
                    table.iloc[idx, col_index] = (value / non_nan_count) * 100
            checked.append(question['qid'])
        else:
            continue
    # return table
