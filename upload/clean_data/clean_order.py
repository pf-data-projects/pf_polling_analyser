"""
Module that contains the clean order function.
"""

import pandas as pd

def clean_order(order):
    """
    Takes the order dataframe as an argument and
    returns a cleaned version with just the question ids
    and questions/answers
    """
    # filters the df by records that pertain to actual questions
    filtered = order[order['Key'].str.contains('q-')]

    # filters out records that are option headers from the df
    filtered = filtered[
        ~filtered['Key'].str.contains('optionheader', case=False)
        ]

    # filters out instructions to select 'other'
    filtered = filtered[
        ~filtered['Key'].str.contains('other', case=False)
        ]

    # filters out disqualification message
    filtered = filtered[
        ~filtered['Key'].str.contains('disqualify', case=False)
        ]

    # added_columns = filter_valid_questions['Opt/Quest.'] = "Question"

    cleaned_dataframe = {
        "QID": [],
        "blank1":[],
        "blank2":[],
        "Question": [],
        "Type": []
    }

    for index, row in filtered.iterrows():
        question_id = row['Key'].split("-")[1]
        cleaned_dataframe['QID'].append(question_id)

        question = row['Default Text']
        cleaned_dataframe['Question'].append(question)

        if "-o-" in row['Key']:
            cleaned_dataframe['Type'].append("Option")
        else:
            cleaned_dataframe['Type'].append("Question")
        cleaned_dataframe['blank1'].append("blank")
        cleaned_dataframe['blank2'].append("blank")

    cleaned_order = pd.DataFrame(cleaned_dataframe)
    cleaned_order = cleaned_order.rename(columns={
        "QID": "question_id",
        "Question": "question_title",
        "Type": "question_text"
    })

    return cleaned_order
