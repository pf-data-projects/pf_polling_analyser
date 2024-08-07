"""
This module rebases the weighted and unweighted totals 
for all rebased questions.

The outer loop iterates over all the questions in the survey.

For each question there is an inner loop which iterates over all
the crossbreaks and calculates the total number of respondents in the
crossbreak for the question.

The output is a dictionary which is stored in memory and downloaded as
a json file.
"""

# import pandas as pd
from . import helpers
from .define_standard_crossbreaks import CROSSBREAKS, QUESTIONS
from .seg import SEG_MAPPING
from .children_age import AGE_QUESTIONS


def rebase_headers(results, question_list, standard_cb, non_standard_cb):
    """
    Write docstring here
    """
    checked = []
    header_data = {}
    results['weighted_respondents'] = results['weighted_respondents'].astype(float)

    # Outer loop: all the survey questions
    for question in question_list:
        column = results[helpers.col_with_substr(results, question['qid'])]
        contains_nan = (column == 'nan').any().any()

        # Logic for multi-select questions
        if question['Base Type'] == 'Question' and (question['type'] == 'CHECKBOX' or question['type'] == 'TABLE' or  question['type'] == 'RANK'):
            checkbox_cols = results[helpers.col_with_qid(results, question['qid'])]
            has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
            if question['qid'] not in checked:
                if has_nan_rows:
                    header_data[question['qid']] = {}

                    sum_figures = find_sums_for_multi(results, results, question['qid'])
                    if sum_figures is not None:
                        header_data[question['qid']]['Total'] = sum_figures

                    # Iterate through standard crossbreaks
                    for key, value in CROSSBREAKS.items():
                        cb_question = QUESTIONS[key]
                        if key in standard_cb:
                            if key == 'children(updated)':
                                for age_question in AGE_QUESTIONS:
                                    get_col = results[helpers.col_substr_partial(results, age_question)]
                                    filtered_df = results.loc[results[get_col.columns[0]] != 'nan']
                                    sum_figures = find_sums_for_multi(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][age_question] = sum_figures
                            elif key == 'seg':
                                segs = CROSSBREAKS['seg']
                                iterations = []
                                for seg in segs:
                                    seg_dict = {
                                        'seg': SEG_MAPPING[seg],
                                        'name': seg
                                    }
                                    iterations.append(seg_dict)
                                for iteration in iterations:
                                    seg_q = 'Think about the Chief Income Earner in your household'
                                    get_seg = results[helpers.col_substr_partial(results, seg_q)]
                                    contains = get_seg.iloc[:, 0].isin(iteration['seg'])
                                    filtered_df = results[contains]
                                    sum_figures = find_sums_for_multi(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][iteration['name']] = sum_figures
                            elif key == 'age':
                                ages = CROSSBREAKS["age"]
                                age_brackets = []
                                for age in ages:
                                    if "-" in age:
                                        num1 = int(age.split("-", 1)[0])
                                        num2 = int(age.split("-", 1)[1])
                                        bracket = {
                                            'num1': num1,
                                            'num2': num2,
                                            'name': age
                                        }
                                        age_brackets.append(bracket)
                                    else:
                                        num1 = int(age.split("+", 1)[0])
                                        num2 = 200
                                        bracket = {
                                            'num1': num1,
                                            'num2': num2,
                                            'name': age
                                        }
                                        age_brackets.append(bracket)
                                for bracket in age_brackets:
                                    age_q = 'How old are you?'
                                    get_age = results[helpers.col_with_substr_q(results, age_q)].astype(float)
                                    filtered_df = results.loc[
                                        (results[get_age.columns[0]].astype(float) >= bracket['num1'])
                                        ]
                                    filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(float) <= bracket['num2'])]
                                    sum_figures = find_sums_for_multi(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][bracket['name']] = sum_figures
                            else:
                                for i in value:
                                    get_cb = results[helpers.col_with_substr_q(results, cb_question)]
                                    filtered_df = results.loc[(results[get_cb.columns[0]] == i)]
                                    sum_figures = find_sums_for_multi(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][i] = sum_figures
                    # Iterate through non-standard crossbreaks
                    if len(non_standard_cb) > 0:
                        for cb in non_standard_cb:
                            crossbreak_q = cb[1]
                            for answer in cb[2]:
                                get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
                                filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
                                sum_figures = find_sums_for_multi(filtered_df, results, question['qid'])
                                if sum_figures is not None:
                                    header_data[question['qid']][answer] = sum_figures
                checked.append(question['qid'])

        elif question['Base Type'] == 'Option' and question['type'] == 'CHECKBOX':
            continue

        elif question['Base Type'] == 'Option' and question['type'] == 'TABLE':
            continue

        elif question['Base Type'] == 'Option' and question['type'] == 'RANK':
            continue

        elif contains_nan and question['type'] == 'RADIO':
            non_nan_count = column[column != 'nan'].count().iloc[0]
            if question['qid'] not in checked:
                if non_nan_count > 0:
                    header_data[question['qid']] = {} # Initialise data for qid
                    # Find rebased totals
                    sum_figures = find_sums_for_single(results, results, question['qid'])
                    if sum_figures is not None:
                        header_data[question['qid']]['Total'] = sum_figures
                    # Iterate through standard crossbreaks
                    for key, value in CROSSBREAKS.items():
                        cb_question = QUESTIONS[key]
                        if key in standard_cb:
                            if key == 'children(updated)':
                                for age_question in AGE_QUESTIONS:
                                    get_col = results[helpers.col_substr_partial(results, age_question)]
                                    filtered_df = results.loc[results[get_col.columns[0]] != 'nan']
                                    sum_figures = find_sums_for_single(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][age_question] = sum_figures
                            elif key == 'age':
                                ages = CROSSBREAKS["age"]
                                age_brackets = []
                                for age in ages:
                                    if "-" in age:
                                        num1 = int(age.split("-", 1)[0])
                                        num2 = int(age.split("-", 1)[1])
                                        bracket = {
                                            'num1': num1,
                                            'num2': num2,
                                            'name': age
                                        }
                                        age_brackets.append(bracket)
                                    else:
                                        num1 = int(age.split("+", 1)[0])
                                        num2 = 200
                                        bracket = {
                                            'num1': num1,
                                            'num2': num2,
                                            'name': age
                                        }
                                        age_brackets.append(bracket)
                                for bracket in age_brackets:
                                    age_q = 'How old are you?'
                                    get_age = results[helpers.col_with_substr_q(results, age_q)].astype(float)
                                    filtered_df = results.loc[
                                        (results[get_age.columns[0]].astype(float) >= bracket['num1'])
                                        ]
                                    filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(float) <= bracket['num2'])]
                                    sum_figures = find_sums_for_single(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][bracket['name']] = sum_figures  
                            elif key == 'seg':
                                segs = CROSSBREAKS['seg']
                                iterations = []
                                for seg in segs:
                                    seg_dict = {
                                        'seg': SEG_MAPPING[seg],
                                        'name': seg
                                    }
                                    iterations.append(seg_dict)
                                for iteration in iterations:
                                    seg_q = 'Think about the Chief Income Earner in your household'
                                    get_seg = results[helpers.col_substr_partial(results, seg_q)]
                                    contains = get_seg.iloc[:, 0].isin(iteration['seg'])
                                    filtered_df = results[contains]
                                    sum_figures = find_sums_for_single(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][iteration['name']] = sum_figures                                    
                            else:
                                for i in value:
                                    get_cb = results[helpers.col_with_substr_q(results, cb_question)]
                                    filtered_df = results.loc[(results[get_cb.columns[0]] == i)]
                                    sum_figures = find_sums_for_single(filtered_df, results, question['qid'])
                                    if sum_figures is not None:
                                        header_data[question['qid']][i] = sum_figures
                                    
                    # Iterate through non-standard crossbreaks
                    if len(non_standard_cb) > 0:
                        for cb in non_standard_cb:
                            crossbreak_q = cb[1]
                            for answer in cb[2]:
                                get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
                                filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
                                sum_figures = find_sums_for_single(filtered_df, results, question['qid'])
                                if sum_figures is not None:
                                    header_data[question['qid']][answer] = sum_figures

                checked.append(question['qid'])
        else:
            checked.append(question['qid'])
            continue
    # print(header_data)
    return header_data


def find_sums_for_multi(filtered_df, results, question_id):
    """
    Logic for filtering the data
    for multiselect questions
    """
    checkbox_cols = filtered_df[helpers.col_with_qid(results, question_id)]
    if question_id == "90":
        checkbox_cols.to_csv("rebase_header_debug.csv")
    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
    if has_nan_rows:
        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
        # print("question", question_id, int(non_nan_count))
        sum1 = int(non_nan_count)

    qid_columns = helpers.col_with_qid(results, question_id)
    selected_columns = qid_columns + ['weighted_respondents']
    checkbox_cols = filtered_df[selected_columns]
    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
    non_nan_rows = ~rows_with_all_nan
    if has_nan_rows:
        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
        sum2 = int(sum2)
    if has_nan_rows:
        return [sum1, sum2]
    else:
        return None


def find_sums_for_single(filtered_df, results, question_id):
    """
    Logic for filtering the data
    for single select questions.
    """
    column = filtered_df[helpers.col_with_substr(results, question_id)]
    non_nan_count = column[column != 'nan'].count().iloc[0]
    column_name = helpers.col_with_substr(results, question_id)[0]
    column = filtered_df[column_name]
    non_nan_rows = column != 'nan'
    if non_nan_count > 0:
        sum1 = int(non_nan_count)
        sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
        sum2 = int(sum2)
        return [sum1, sum2]
    else:
        return None
