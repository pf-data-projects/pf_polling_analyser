import pandas as pd

from . import define_standard_crossbreaks as cb

def calc_gender(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    gender_q = 'Which of the following best describes how you think of yourself?'
    for question in question_list:
        get_gender = results[cb.columns_with_substring_question(results, gender_q)]
        filtered_df = results.loc[(results[get_gender.columns[0]] == category)]
        table.iat[0, col_index] = len(filtered_df.index)

        if question['Base Type'] == 'Question' and question['type'] == 'CHECKBOX':
            options_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'Option')
            ]
            options = options_df['question_title'].tolist()
            for option in options:
                filtered_df_len = filtered_df[cb.columns_with_substring_answers(results, option, question['qid'])].count()
                responses = int(filtered_df_len.iloc[0])
                position = table[(
                    table['Answers'] == option
                ) & (
                    table['IDs'] == question['qid']
                )].index
                # Checks that this exists in the table.
                position_int = int(position[0])
                table.iat[position_int, col_index] = responses

        elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
            continue

        elif question['Base Type'] == 'Question' and question['type'] == 'TABLE':
            sub_questions_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'sub_Question')
            ]
            sub_questions = sub_questions_df['question_title'].tolist()
            options_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'Option')
            ]
            options = options_df['question_title'].tolist()
            for sub_question in sub_questions:
                table_filtered_df = filtered_df[cb.columns_with_substring_answers(results, sub_question, question['qid'])]
                i = 1
                for option in options:
                    responses_df = (table_filtered_df == option).sum()
                    responses = int(responses_df.iloc[0])
                    sub_question_position = table[(
                        table['Answers'] == sub_question
                    ) & (
                        table['IDs'] == question['qid']
                    )].index
                    sq_position_int = int(sub_question_position[0]) + i
                    table.iat[sq_position_int, col_index] = responses
                    i += 1

        elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
            continue

        else:
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
                    for i, option in enumerate(options):
                        second_filtered_df = filtered_df[filtered_df.iloc[:, 0] == options[i]]
                        position = table[(
                            table['Answers'] == options[i]
                        ) & (
                            table['IDs'] == question['qid']
                        )].index
                        # print(options[i])
                        # print(question['qid'])
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
    print(table.head(20))
    print(category, "done!")
    return table
