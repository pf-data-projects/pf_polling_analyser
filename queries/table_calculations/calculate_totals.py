"""This file controls all the logic for the calculations of totals/crossbreaks/rebasing"""

# import os
import json
# import pandas as pd
from django.core.cache import cache
from .create_blank_table import create_blank_table
from .age import iterate_age_brackets, iterate_age_rebase
from .seg import iterate_seg, iterate_seg_rebase
from .children_age import iterate_over_children_ages, rebase_children_ages
from .define_standard_crossbreaks import CROSSBREAKS, QUESTIONS, calc_standard, rebase_standard
from .define_non_standard_cb import calc_crossbreak, rebase_crossbreak
from .calc import calc
from .rebase import rebase
from .rebase_headers import rebase_headers


def table_calculation(self, results, question_data, standard_cb, non_standard_cb):
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

    question_list = [d for d in question_list if d['Base Type'] == 'Question']

    actual_total = len(results.index)
    weighted_total = results['weighted_respondents'].astype(float).sum()
    adjustment = actual_total / weighted_total

    results['weighted_respondents'] = results['weighted_respondents'].astype(float) * adjustment
    results = results.astype(str)

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
        self.update_state(
            state='PROGRESS',
            meta={'Totals': 'Calculating totals'}
        )
        table = calc(results, 5, table, question, results, question_data, True)

    # calculations for standard crossbreaks
    k = 0
    self.update_state(
        state='PROGRESS',
        meta={'StandardCB': k, 'total': len(standard_cb)}
    )
    for key, value in CROSSBREAKS.items():
        question = QUESTIONS[key]
        if key in standard_cb:
            if key == 'age':
                table = iterate_age_brackets(
                    table, question_list, results, question_data)
                self.update_state(
                    state='PROGRESS',
                    meta={'StandardCB': k + 1, 'total': len(standard_cb)}
                )
                k += 1
                continue
            if key == 'seg':
                table = iterate_seg(table, question_list, results, question_data)
                self.update_state(
                    state='PROGRESS',
                    meta={'StandardCB': k + 1, 'total': len(standard_cb)}
                )
                k += 1
                continue
            if key == 'children(updated)':
                table = iterate_over_children_ages(
                    table, question_list, results, question_data
                )
                self.update_state(
                    state='PROGRESS',
                    meta={'StandardCB': k + 1, 'total': len(standard_cb)}
                )
                k += 1
                continue
            for i in value:
                table = calc_standard(
                    i,
                    table.columns.get_loc(i),
                    question,
                    table,
                    question_list,
                    results,
                    question_data,
                )
        else:
            continue
        # ||||||||||||||||||||||||| CELERY ||||||||||||||||||||||||||||
        self.update_state(
            state='PROGRESS',
            meta={'StandardCB': k + 1, 'total': len(standard_cb)}
        )
        k += 1

    # Run calc for any non standard crossbreaks.
    k = 0
    if len(non_standard_cb) > 0:
        self.update_state(
            state='PROGRESS',
            meta={'nonStandardCB': k, 'total': len(non_standard_cb)}
        )
        for crossbreak in non_standard_cb:
            calc_crossbreak(table, question_list, results, question_data, crossbreak)
            # ||||||||||||||||||||||||| CELERY ||||||||||||||||||||||||||||
            self.update_state(
                state='PROGRESS',
                meta={'nonStandardCB': k + 1, 'total': len(non_standard_cb)}
            )
            k += 1

    # # adjust weighted totals so that they are a proportion of actual total
    # adjustment_ratio = table.loc[0, 'Total'] / table.loc[1, 'Total']

    # # Determine numeric columns starting from the fifth column onward
    # is_numeric = table.iloc[1, 4:].apply(lambda x: isinstance(x, (int, float)))
    # numeric_cols = table.columns[4:][is_numeric]

    # # Adjust only the numeric columns in the "Weighted" row
    # table.loc[1, numeric_cols] = table.loc[1, numeric_cols] * adjustment_ratio

    # Display all values as a percentage of the total for each crossbreak.
    weighted_totals = table.iloc[1, 5:]
    table.iloc[2:, 5:] = table.iloc[2:, 5:].div(weighted_totals) * 100

    # Get rebased values for totals column.
    table = rebase(question_data, results, question_list, table, 5)
    # print("main rebase done")

    # rebase calculations for standard crossbreaks
    k = 0
    self.update_state(
        state='PROGRESS',
        meta={'rebaseStandardCB': k, 'total': len(standard_cb)}
    )
    for key, value in CROSSBREAKS.items():
        question = QUESTIONS[key]
        if key in standard_cb:
            if key == 'age':
                table = iterate_age_rebase(
                    table, question_list, results, question_data)
                self.update_state(
                    state='PROGRESS',
                    meta={'rebaseStandardCB': k + 1, 'total': len(standard_cb)}
                )
                continue
            if key == 'seg':
                table = iterate_seg_rebase(
                    table, question_list, results, question_data)
                self.update_state(
                    state='PROGRESS',
                    meta={'rebaseStandardCB': k + 1, 'total': len(standard_cb)}
                )
                continue
            if key == 'children(updated)':
                table = rebase_children_ages(
                    table, question_list, results, question_data
                )
                self.update_state(
                    state='PROGRESS',
                    meta={'rebaseStandardCB': k + 1, 'total': len(standard_cb)}
                )
                continue
            for i in value:
                table = rebase_standard(
                    i,
                    table.columns.get_loc(i),
                    question,
                    table,
                    question_list,
                    results,
                    question_data
                )
        else:
            continue
        # ||||||||||||||||||||||||| CELERY ||||||||||||||||||||||||||||
        self.update_state(
            state='PROGRESS',
            meta={'rebaseStandardCB': k + 1, 'total': len(standard_cb)}
        )
        k += 1

    # rebase non-standard crossbreak calculations
    k = 0
    if len(non_standard_cb) > 0:
        self.update_state(
            state='PROGRESS',
            meta={'rebaseNonStandardCB': k, 'total': len(non_standard_cb)}
        )
        for crossbreak in non_standard_cb:
            rebase_crossbreak(
                table, question_list, results, question_data, crossbreak)
            # ||||||||||||||||||||||||| CELERY ||||||||||||||||||||||||||||
            self.update_state(
                state='PROGRESS',
                meta={'rebaseNonStandardCB': k + 1, 'total': len(non_standard_cb)}
            )
            k += 1

    # ||||||||||||||||||||||||| CELERY ||||||||||||||||||||||||||||
    self.update_state(
        state='PROGRESS',
        meta={'CreatingHeaders': 'Creating rebased column headers...'}
    )
    rebased_header_data = rebase_headers(results, question_list, standard_cb, non_standard_cb)
    rebased_json = json.dumps(rebased_header_data)
    cache_key = 'rebase_json'
    cache.set(cache_key, rebased_json, 300)

    return [table, rebased_json]
