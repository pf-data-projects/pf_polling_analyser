import pandas as pd

from . import define_standard_crossbreaks as cb


def calc_region(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    region_q = 'In what region of the UK do you live?'
    for question in question_list:
        get_gender = results[cb.columns_with_substring_question(results, region_q)]
        filtered_df = results.loc[(results[get_gender.columns[0]] == category)]
        filtered_df = filtered_df[cb.columns_with_substring(results, question['qid'])]
        # checks that question exists in responses.
        if not filtered_df.empty:
            all_options = question_data.loc[(question_data['question_text'] == 'Option')]
            relevant_options = all_options.loc[
                (all_options['question_id'] == int(question['qid']))
            ]
            if len(relevant_options.index) == 0:
                relevant_options = all_options.loc[
                    (all_options['question_id'] == question['qid'])
                ]
            options = relevant_options['question_title'].tolist()
            # checks that there are options for the question.
            # E.G. Age crossbreak question has no options.
            if len(options) > 0:
                for j, option in enumerate(options):
                    second_filtered_df = filtered_df[filtered_df.iloc[:, 0] == options[j]]
                    position = table[(
                        table['Answers'] == options[j]
                    ) & (
                        table['IDs'] == question['qid']
                    )].index

                    # Checks that this exists in the table.
                    # I think the different indexers for
                    # different loops are not quite the same.
                    if len(position) > 0:
                        position_int = int(position[0])
                        table.iat[position_int, col_index] = len(second_filtered_df.index)
                    else:
                        continue
            else:
                continue
        else:
            continue
    # print(table.head(20))
    # table.to_csv('region.csv', encoding="utf-8-sig", index=False)
    print(category, "done!")
    return table


def iterate_regions(table, question_list, results, question_data):
    """
    Loops through the list of regions and
    builds a list of dictionaries which
    contain the necessary arguments for a call
    of the calc_region function.
    """
    regions = cb.REGION
    table_col = 11
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
