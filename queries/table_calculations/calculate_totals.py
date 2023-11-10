import os
import pandas as pd
from .create_blank_table import create_blank_table
from .helpers import (
    col_with_substr,
    col_with_substr_a
    )
from .gender import calc_gender, gender_rebase
from .age import iterate_age_brackets, iterate_age_rebase
from .region import iterate_regions, iterate_regions_rebase
from .seg import iterate_seg, iterate_seg_rebase
from .children import calc_children, children_rebase
from .education import iterate_ed, iterate_ed_rebase
from .define_non_standard_cb import calc_crossbreak, rebase_crossbreak
from .rebase import rebase

def table_calculation(results, question_data, standard_cb, non_standard_cb):
    """
    A function that controls the flow of logic for the
    creation of the table.
    """
    # make sure all results are in string format.
    results = results.astype(str)

    # Builds a dictionary used to iterate over all questions/answers
    table = create_blank_table(question_data, standard_cb, non_standard_cb)
    questions = table['Answers'].tolist()
    question_ids = table['IDs'].tolist()
    question_types = table['Types'].tolist()
    question_rebase = table['Rebase comment needed'].tolist()
    question_base_type = table['Base Type'].tolist()

    question_list = []
    for i in range(len(questions)):
        item = {
            'qid': f'{question_ids[i]}',
            'question': questions[i],
            'type': question_types[i],
            'rebase': question_rebase[i],
            'Base Type': question_base_type[i]
        }
        question_list.append(item)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work out the totals for each question

    # loops through all question options to find
    # number of respondents who answered each question a certain way
    for question in question_list:
        if question['qid'] == "Total":
            continue
        if question['qid'] == "Weighted":
            continue
        # adds the total respondents to table
        table.iat[0, 5] = len(results.index)
        table.iat[1, 5] = results['weighted_respondents'].astype(float).sum()

        # ~~~~~~~~~~~~~ Calculates responses for checkbox/multiselect questions

        if question['Base Type'] == 'Question' and question['type'] == 'CHECKBOX':
            options_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'Option')
            ]
            options = options_df['question_title'].tolist()
            for option in options:
                checkbox_filtered_df = results[col_with_substr_a(results, option, question['qid'])]
                if checkbox_filtered_df.empty:
                    continue
                responses_df = (checkbox_filtered_df == option).sum()
                responses = int(responses_df.iloc[0])
                # finds the position in the table to add the data
                position = table[(
                    table['Answers'] == option
                ) & (
                    table['IDs'] == question['qid']
                )].index
                # Checks that this exists in the table.
                position_int = int(position[0])
                table.iat[position_int, 5] = responses

        elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
            continue

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for table questions

        elif question['Base Type'] == 'Question' and question['type'] == 'TABLE':
            sub_questions_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'sub_Question')
            ]
            sub_questions = sub_questions_df['question_title'].tolist()
            options_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_type'] == 'TABLE') &
                (question_data['question_text'] == 'Option')
            ]
            options_list = options_df['question_title'].tolist()
            options = list(dict.fromkeys(options_list))
            for sub_question in sub_questions:
                table_filtered_df = results[col_with_substr_a(results, sub_question, question['qid'])]
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
                    table.iat[sq_position_int, 5] = responses
                    i += 1

        elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
            continue

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Calculates responses for rank questions

        elif question['Base Type'] == 'Question' and question['type'] == 'RANK':
            sub_questions_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_text'] == 'Option')
            ]
            sub_questions = sub_questions_df['question_title'].tolist()
            options_df = question_data[
                (question_data['question_id'] == int(question['qid'])) &
                (question_data['question_type'] == 'RANK') &
                (question_data['question_text'] == 'sub_option')
            ]
            options_list = options_df['question_title'].tolist()
            options = list(dict.fromkeys(options_list))
            for sub_question in sub_questions:
                table_filtered_df = results[col_with_substr_a(results, sub_question, question['qid'])]
                table_filtered_df = table_filtered_df.astype(float)
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
                    table.iat[sq_position_int, 5] = responses
                    i += 1

        elif question['Base Type'] == 'Option' and question['type'] == 'Rank':
            continue

        # ~~~~~~~ Calculates responses for Single-select radio button questions

        else:
            # finds column that contains question id
            filtered_df = results[col_with_substr(results, question['qid']) + ['weighted_respondents']]
            # checks that question exists in responses.
            if not filtered_df.empty:
                all_options = question_data.loc[
                    (question_data['question_text'] == 'Option')
                    ]
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
                        second_filtered_df = filtered_df[
                            filtered_df.iloc[:, 0] == options[i]
                            ]
                        position = table[(
                            table['Answers'] == options[i]
                        ) & (
                            table['IDs'] == question['qid']
                        )].index
                        # Checks that this exists in the table.
                        if len(position) > 0:
                            position_int = int(position[0])
                            table.iat[position_int, 5] = len(second_filtered_df.index)
                        else:
                            continue
                else:
                    continue
            else:
                continue
    # Run calculations for standard crossbreaks
    if 'gender' in standard_cb:
        print("---- PROCESSING GENDER CROSSBREAKS ----")
        table = calc_gender(
            "Male", 
            table.columns.get_loc('Male'),
            table,
            question_list,
            results,
            question_data
        )
        table = calc_gender(
            "Female", 
            table.columns.get_loc('Female'),
            table,
            question_list,
            results,
            question_data
        )
    if 'age' in standard_cb:
        print("---- PROCESSING AGE CROSSBREAKS ----")
        table = iterate_age_brackets(
            table, question_list, results, question_data)
    if 'region' in standard_cb:
        print("---- PROCESSING REGION CROSSBREAKS ----")
        table = iterate_regions(table, question_list, results, question_data)
    if 'seg' in standard_cb:
        print("---- PROCESSING SEG CROSSBREAKS ----")
        table = iterate_seg(table, question_list, results, question_data)
    if 'education' in standard_cb:
        print("--- PROCESSING EDUCATION CROSSBREAKS ---")
        table = iterate_ed(table, question_list, results, question_data)
    if 'children' in standard_cb:
        print("---- PROCESSING CHILDREN CROSSBREAKS ----")
        table = calc_children(
            "Yes", 
            table.columns.get_loc('Yes'),
            table,
            question_list,
            results,
            question_data
        )
        table = calc_children(
            "No", 
            table.columns.get_loc('No'),
            table,
            question_list,
            results,
            question_data
        )
    # Run calc for any non standard crossbreaks.
    if len(non_standard_cb) > 0:
        for crossbreak in non_standard_cb:
            calc_crossbreak(table, question_list, results, question_data, crossbreak)

    # adjust weighted totals so that they are a proportion of actual total
    adjustment_ratio = table.loc[0, 'Total'] / table.loc[1, 'Total']

    # Determine numeric columns starting from the fifth column onward
    is_numeric = table.iloc[1, 4:].apply(lambda x: isinstance(x, (int, float)))
    numeric_cols = table.columns[4:][is_numeric]

    # Adjust only the numeric columns in the "Weighted" row
    table.loc[1, numeric_cols] = table.loc[1, numeric_cols] * adjustment_ratio

    # Display all values as a percentage of the total for each crossbreak.
    weighted_totals = table.iloc[1, 5:]
    table.iloc[2:, 5:] = table.iloc[2:, 5:].div(weighted_totals) * 100

    # Get rebased values for totals column.
    table = rebase(question_data, results, question_list, table, 5)

    # Iterate through standard crossbreaks to rebase any questions that need it.
    if 'gender' in standard_cb:
        table = gender_rebase(
            "Male", 
            table.columns.get_loc('Male'),
            table,
            question_list,
            results,
            question_data
        )
        table = gender_rebase(
            "Female", 
            table.columns.get_loc('Female'),
            table,
            question_list,
            results,
            question_data
        )
    if 'age' in standard_cb:
        table = iterate_age_rebase(
            table, question_list, results, question_data)
    if 'region' in standard_cb:
        table = iterate_regions_rebase(
            table, question_list, results, question_data)
    if 'seg' in standard_cb:
        table = iterate_seg_rebase(
            table, question_list, results, question_data)
    if 'education' in standard_cb:
        table = iterate_ed_rebase(
            table, question_list, results, question_data)
    if 'children' in standard_cb:
        table = children_rebase(
            "Yes",
            table.columns.get_loc('Yes'),
            table,
            question_list,
            results,
            question_data
        )
        table = children_rebase(
            "No", 
            table.columns.get_loc('No'),
            table,
            question_list,
            results,
            question_data
        )
    if len(non_standard_cb) > 0:
        for crossbreak in non_standard_cb:
            rebase_crossbreak(
                table, question_list, results, question_data, crossbreak)

    return table
