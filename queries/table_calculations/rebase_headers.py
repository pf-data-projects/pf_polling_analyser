"""Rebases the column headers"""

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
                    header_data[question['qid']] = {} # Initialise data for qid
                    # rebased totals
                    checkbox_cols = results[helpers.col_with_qid(results, question['qid'])]
                    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                    if has_nan_rows:
                        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                        sum1 = int(non_nan_count)
                    qid_columns = helpers.col_with_qid(results, question['qid'])
                    selected_columns = qid_columns + ['weighted_respondents']
                    checkbox_cols = results[selected_columns]
                    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                    non_nan_rows = ~rows_with_all_nan
                    if has_nan_rows:
                        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                        sum2 = int(sum2)
                        header_data[question['qid']]['Total'] = [sum1, sum2]
                    # Iterate through standard crossbreaks
                    for key, value in CROSSBREAKS.items():
                        cb_question = QUESTIONS[key]
                        if key in standard_cb:
                            if key == 'children(updated)':
                                for age_question in AGE_QUESTIONS:
                                    get_col = results[helpers.col_substr_partial(results, age_question)]
                                    filtered_df = results.loc[results[get_col.columns[0]] != 'nan']
                                    checkbox_cols = filtered_df[helpers.col_with_qid(results, question['qid'])]
                                    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                                    if has_nan_rows:
                                        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                                        sum1 = int(non_nan_count)
                                    qid_columns = helpers.col_with_qid(results, question['qid'])
                                    selected_columns = qid_columns + ['weighted_respondents']
                                    checkbox_cols = filtered_df[selected_columns]
                                    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                                    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                                    non_nan_rows = ~rows_with_all_nan
                                    if has_nan_rows:
                                        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][age_question] = [sum1, sum2]
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
                                    checkbox_cols = filtered_df[helpers.col_with_qid(results, question['qid'])]
                                    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                                    if has_nan_rows:
                                        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                                        sum1 = int(non_nan_count)
                                    qid_columns = helpers.col_with_qid(results, question['qid'])
                                    selected_columns = qid_columns + ['weighted_respondents']
                                    checkbox_cols = filtered_df[selected_columns]
                                    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                                    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                                    non_nan_rows = ~rows_with_all_nan
                                    if has_nan_rows:
                                        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][iteration['name']] = [sum1, sum2]
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
                                    get_age = results[helpers.col_with_substr_q(results, age_q)].astype(int)
                                    filtered_df = results.loc[
                                        (results[get_age.columns[0]].astype(int) >= bracket['num1'])
                                        ]
                                    filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(int) <= bracket['num2'])]
                                    checkbox_cols = filtered_df[helpers.col_with_qid(results, question['qid'])]
                                    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                                    if has_nan_rows:
                                        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                                        sum1 = int(non_nan_count)
                                    qid_columns = helpers.col_with_qid(results, question['qid'])
                                    selected_columns = qid_columns + ['weighted_respondents']
                                    checkbox_cols = filtered_df[selected_columns]
                                    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                                    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                                    non_nan_rows = ~rows_with_all_nan
                                    if has_nan_rows:
                                        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][bracket['name']] = [sum1, sum2]
                            else:
                                for i in value:
                                    get_cb = results[helpers.col_with_substr_q(results, cb_question)]
                                    filtered_df = results.loc[(results[get_cb.columns[0]] == i)]
                                    checkbox_cols = filtered_df[helpers.col_with_qid(results, question['qid'])]
                                    has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                                    if has_nan_rows:
                                        non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                                        sum1 = int(non_nan_count)
                                    qid_columns = helpers.col_with_qid(results, question['qid'])
                                    selected_columns = qid_columns + ['weighted_respondents']
                                    checkbox_cols = filtered_df[selected_columns]
                                    nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                                    rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                                    non_nan_rows = ~rows_with_all_nan
                                    if has_nan_rows:
                                        sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][i] = [sum1, sum2]
                    # Iterate through non-standard crossbreaks
                    if len(non_standard_cb) > 0:
                        for cb in non_standard_cb:
                            crossbreak_q = cb[1]
                            for answer in cb[2]:
                                get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
                                filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
                                checkbox_cols = filtered_df[helpers.col_with_qid(results, question['qid'])]
                                has_nan_rows = (checkbox_cols == 'nan').all(axis=1).any()
                                if has_nan_rows:
                                    non_nan_count = (checkbox_cols != 'nan').any(axis=1).sum()
                                    sum1 = int(non_nan_count)
                                qid_columns = helpers.col_with_qid(results, question['qid'])
                                selected_columns = qid_columns + ['weighted_respondents']
                                checkbox_cols = filtered_df[selected_columns]
                                nan_check_cols = checkbox_cols.drop(columns=['weighted_respondents'])
                                rows_with_all_nan = nan_check_cols.apply(lambda x: x.astype(str).eq('nan').all(), axis=1)
                                non_nan_rows = ~rows_with_all_nan
                                if has_nan_rows:
                                    sum2 = checkbox_cols.loc[non_nan_rows, 'weighted_respondents'].sum()
                                    sum2 = int(sum2)
                                    header_data[question['qid']][answer] = [sum1, sum2]
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
                    column = results[helpers.col_with_substr(results, question['qid'])]
                    non_nan_count = column[column != 'nan'].count().iloc[0]
                    column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                    column = results[column_name]
                    non_nan_rows = column != 'nan'
                    if non_nan_count > 0:
                        sum1 = int(non_nan_count)
                        sum2 = results.loc[non_nan_rows, 'weighted_respondents'].sum()
                        sum2 = int(sum2)
                        header_data[question['qid']]['Total'] = [sum1, sum2]
                    # Iterate through standard crossbreaks
                    for key, value in CROSSBREAKS.items():
                        cb_question = QUESTIONS[key]
                        if key in standard_cb:
                            if key == 'children(updated)':
                                for age_question in AGE_QUESTIONS:
                                    get_col = results[helpers.col_substr_partial(results, age_question)]
                                    filtered_df = results.loc[results[get_col.columns[0]] != 'nan']
                                    column = filtered_df[helpers.col_with_substr(results, question['qid'])]
                                    non_nan_count = column[column != 'nan'].count().iloc[0]
                                    column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                                    column = filtered_df[column_name]
                                    non_nan_rows = column != 'nan'
                                    if non_nan_count > 0:
                                        sum1 = int(non_nan_count)
                                        sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][age_question] = [sum1, sum2]
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
                                    get_age = results[helpers.col_with_substr_q(results, age_q)].astype(int)
                                    filtered_df = results.loc[
                                        (results[get_age.columns[0]].astype(int) >= bracket['num1'])
                                        ]
                                    filtered_df = filtered_df.loc[(filtered_df[get_age.columns[0]].astype(int) <= bracket['num2'])]
                                    column = filtered_df[helpers.col_with_substr(results, question['qid'])]
                                    non_nan_count = column[column != 'nan'].count().iloc[0]
                                    column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                                    column = filtered_df[column_name]
                                    non_nan_rows = column != 'nan'
                                    if non_nan_count > 0:
                                        sum1 = int(non_nan_count)
                                        sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][bracket['name']] = [sum1, sum2]
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
                                    column = filtered_df[helpers.col_with_substr(results, question['qid'])]
                                    non_nan_count = column[column != 'nan'].count().iloc[0]
                                    column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                                    column = filtered_df[column_name]
                                    non_nan_rows = column != 'nan'
                                    if non_nan_count > 0:
                                        sum1 = int(non_nan_count)
                                        sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][iteration['name']] = [sum1, sum2]
                            else:
                                for i in value:
                                    get_cb = results[helpers.col_with_substr_q(results, cb_question)]
                                    filtered_df = results.loc[(results[get_cb.columns[0]] == i)]
                                    column = filtered_df[helpers.col_with_substr(results, question['qid'])]
                                    non_nan_count = column[column != 'nan'].count().iloc[0]
                                    column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                                    column = filtered_df[column_name]
                                    non_nan_rows = column != 'nan'
                                    if non_nan_count > 0:
                                        sum1 = int(non_nan_count)
                                        sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
                                        sum2 = int(sum2)
                                        header_data[question['qid']][i] = [sum1, sum2]
                    # Iterate through non-standard crossbreaks
                    if len(non_standard_cb) > 0:
                        for cb in non_standard_cb:
                            crossbreak_q = cb[1]
                            for answer in cb[2]:
                                get_crossbreak = results[helpers.col_with_substr_q(results, crossbreak_q)]
                                filtered_df = results.loc[(results[get_crossbreak.columns[0]] == answer)]
                                column = filtered_df[helpers.col_with_substr(results, question['qid'])]
                                non_nan_count = column[column != 'nan'].count().iloc[0]
                                column_name = helpers.col_with_substr(results, question['qid'])[0]  # Select the first column name
                                column = filtered_df[column_name]
                                non_nan_rows = column != 'nan'
                                if non_nan_count > 0:
                                    sum1 = int(non_nan_count)
                                    sum2 = filtered_df.loc[non_nan_rows, 'weighted_respondents'].sum()
                                    sum2 = int(sum2)
                                    header_data[question['qid']][answer] = [sum1, sum2]
                checked.append(question['qid'])
        else:
            checked.append(question['qid'])
            continue
    # print(header_data)
    return header_data
