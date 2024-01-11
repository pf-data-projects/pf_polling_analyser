"""
This is a helper module that enables any
crossbreak to be calculated in the table.
"""

from . import helpers

def calc(filtered_df, col_index, table, question, results, question_data):
    """
    This function checks the question type and calulates
    the number of respondents who answered a particular way
    """
    # ~~~~~~~~~~~~~ Calculates responses for checkbox/multiselect questions
    if question['qid'] == "Total":
        return table
    if question['qid'] == "Weighted":
        return table

    if question['Base Type'] == 'Question' and question['type'] == 'CHECKBOX':
        options_df = question_data[
            (question_data['question_id'] == int(question['qid'])) &
            (question_data['question_text'] == 'Option')
        ]
        options = options_df['question_title'].tolist()
        for option in options:
            checkbox_filtered_df = filtered_df[helpers.col_with_substr_a(results, option, question['qid']) + ['weighted_respondents']]
            if checkbox_filtered_df.empty:
                continue
            responses_df = checkbox_filtered_df[checkbox_filtered_df.iloc[:, 0] == option]
            responses_df.loc[:, 'weighted_respondents'] = responses_df['weighted_respondents'].astype(float)
            responses = responses_df['weighted_respondents'].sum()
            position = table[(
                table['Answers'] == option
            ) & (
                table['IDs'] == question['qid']
            )].index
            # Checks that this exists in the table.
            position_int = int(position[0])
            table.iat[position_int, col_index] = responses
        return table

    # elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
    #     return table

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for table questions

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
        options_list = options_df['question_title'].tolist()
        options = list(dict.fromkeys(options_list))

        for sub_question in sub_questions:
            table_filtered_df = filtered_df[helpers.col_with_substr_a(results, sub_question, question['qid']) + ['weighted_respondents']]
            i = 1
            for option in options:
                responses_df = table_filtered_df[table_filtered_df.iloc[:, 0] == option]
                responses_df.loc[:, 'weighted_respondents'] = responses_df['weighted_respondents'].astype(float)
                responses = responses_df['weighted_respondents'].sum()
                sub_question_position = table[(
                    table['Answers'] == sub_question
                ) & (
                    table['IDs'] == question['qid']
                )].index
                sq_position_int = int(sub_question_position[0]) + i
                table.iat[sq_position_int, col_index] = responses
                i += 1
        return table

    # elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
    #     return table

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for rank questions

    elif question['Base Type'] == 'Question' and question['type'] == 'RANK':
        sub_questions_df = question_data[
            (question_data['question_id'] == int(question['qid'])) &
            (question_data['question_text'] == 'Option')
        ]
        sub_questions = sub_questions_df['question_title'].tolist()
        options_df = question_data[
            (question_data['question_id'] == int(question['qid'])) &
            (question_data['question_text'] == 'sub_option')
        ]
        options_list = options_df['question_title'].tolist()
        options = list(dict.fromkeys(options_list))
        for sub_question in sub_questions:
            table_filtered_df = filtered_df[helpers.col_with_substr_a(results, sub_question, question['qid']) + ['weighted_respondents']]
            table_filtered_df = table_filtered_df.astype(float)
            i = 1
            for option in options:
                responses_df = table_filtered_df[table_filtered_df.iloc[:, 0] == option]
                responses_df.loc[:, 'weighted_respondents'] = responses_df['weighted_respondents'].astype(float)
                responses = responses_df['weighted_respondents'].sum()
                sub_question_position = table[(
                    table['Answers'] == sub_question
                ) & (
                    table['IDs'] == question['qid']
                )].index
                sq_position_int = int(sub_question_position[0]) + i
                table.iat[sq_position_int, col_index] = responses
                i += 1
        return table

    # elif question['Base Type'] == 'Option' and question['type'] == 'Rank':
    #     return table

    # ~~~~~~~ Calculates responses for Single-select radio button questions

    else:
        filtered_df = filtered_df[helpers.col_with_substr(results, question['qid']) + ['weighted_respondents']]
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
                    # Checks that this exists in the table.
                    # I think the different indexers for
                    # different loops are not quite the same.
                    if len(position) > 0:
                        position_int = int(position[0])
                        table.iat[position_int, col_index] = len(second_filtered_df.index)
                        table.iat[position_int, col_index] = second_filtered_df['weighted_respondents'].astype(float).sum()
                    else:
                        pass
                return table
            else:
                return table
        else:
            return table
