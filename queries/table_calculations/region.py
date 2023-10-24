import pandas as pd

from . import define_standard_crossbreaks as cb
from . import helpers
from . import calc

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

        # ~~~~~~~~~~~~~ Calculates responses for checkbox/multiselect questions

#         if question['Base Type'] == 'Question' and question['type'] == 'CHECKBOX':
#                 options_df = question_data[
#                     (question_data['question_id'] == int(question['qid'])) &
#                     (question_data['question_text'] == 'Option')
#                 ]
#                 options = options_df['question_title'].tolist()
#                 for option in options:
#                     checkbox_filtered_df = filtered_df[cb.columns_with_substring_answers(results, option, question['qid'])]
#                     if checkbox_filtered_df.empty:
#                         continue
#                     responses_df = (checkbox_filtered_df == option).sum()
#                     responses = int(responses_df.iloc[0])
#                     position = table[(
#                         table['Answers'] == option
#                     ) & (
#                         table['IDs'] == question['qid']
#                     )].index
#                     # Checks that this exists in the table.
#                     position_int = int(position[0])
#                     table.iat[position_int, col_index] = responses

#         elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
#             continue

#         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for table questions

#         elif question['Base Type'] == 'Question' and question['type'] == 'TABLE':
#             sub_questions_df = question_data[
#                 (question_data['question_id'] == int(question['qid'])) &
#                 (question_data['question_text'] == 'sub_Question')
#             ]
#             sub_questions = sub_questions_df['question_title'].tolist()
#             options_df = question_data[
#                 (question_data['question_id'] == int(question['qid'])) &
#                 (question_data['question_text'] == 'Option')
#             ]
#             options_list = options_df['question_title'].tolist()
#             options = list(dict.fromkeys(options_list))
#             for sub_question in sub_questions:
#                 table_filtered_df = filtered_df[cb.columns_with_substring_answers(results, sub_question, question['qid'])]
#                 i = 1
#                 for option in options:
#                     responses_df = (table_filtered_df == option).sum()
#                     responses = int(responses_df.iloc[0])
#                     sub_question_position = table[(
#                         table['Answers'] == sub_question
#                     ) & (
#                         table['IDs'] == question['qid']
#                     )].index
#                     sq_position_int = int(sub_question_position[0]) + i
#                     table.iat[sq_position_int, col_index] = responses
#                     i += 1

#         elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
#             continue

#         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for rank questions

#         elif question['Base Type'] == 'Question' and question['type'] == 'RANK':
#             sub_questions_df = question_data[
#                 (question_data['question_id'] == int(question['qid'])) &
#                 (question_data['question_text'] == 'Option')
#             ]
#             sub_questions = sub_questions_df['question_title'].tolist()
#             options_df = question_data[
#                 (question_data['question_id'] == int(question['qid'])) &
#                 (question_data['question_text'] == 'sub_option')
#             ]
#             options_list = options_df['question_title'].tolist()
#             options = list(dict.fromkeys(options_list))
#             for sub_question in sub_questions:
#                 table_filtered_df = filtered_df[cb.columns_with_substring_answers(results, sub_question, question['qid'])]
#                 i = 1
#                 for option in options:
#                     responses_df = (table_filtered_df == option).sum()
#                     responses = int(responses_df.iloc[0])
#                     sub_question_position = table[(
#                         table['Answers'] == sub_question
#                     ) & (
#                         table['IDs'] == question['qid']
#                     )].index
#                     sq_position_int = int(sub_question_position[0]) + i
#                     table.iat[sq_position_int, col_index] = responses
#                     i += 1

#         elif question['Base Type'] == 'Option' and question['type'] == 'Rank':
#             continue

#         # ~~~~~~~ Calculates responses for Single-select radio button questions

#         else:
#             filtered_df = filtered_df[cb.columns_with_substring(results, question['qid'])]
#             # checks that question exists in responses.
#             if not filtered_df.empty:
#                 all_options = question_data.loc[(question_data['question_text'] == 'Option')]
#                 relevant_options = all_options.loc[
#                     (all_options['question_id'] == int(question['qid']))
#                 ]
#                 if len(relevant_options.index) == 0:
#                     relevant_options = all_options.loc[
#                         (all_options['question_id'] == question['qid'])
#                     ]
#                 options = relevant_options['question_title'].tolist()
#                 # checks that there are options for the question.
#                 # E.G. Age crossbreak question has no options.
#                 if len(options) > 0:
#                     for j, option in enumerate(options):
#                         second_filtered_df = filtered_df[filtered_df.iloc[:, 0] == options[j]]
#                         position = table[(
#                             table['Answers'] == options[j]
#                         ) & (
#                             table['IDs'] == question['qid']
#                         )].index

#                         # Checks that this exists in the table.
#                         # I think the different indexers for
#                         # different loops are not quite the same.
#                         if len(position) > 0:
#                             position_int = int(position[0])
#                             table.iat[position_int, col_index] = len(second_filtered_df.index)
#                         else:
#                             continue
#                 else:
#                     continue
#             else:
#                 continue
#     print(category, "done!")
#     return table


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
