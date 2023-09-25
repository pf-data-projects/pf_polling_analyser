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
    print(filtered)

    # filters out records that are option headers from the df
    filtered = filtered[
        ~filtered['Key'].str.contains('optionheader', case=False)
        ]
    print(filtered)

    # filters out instructions to select 'other'
    filtered = filtered[
        ~filtered['Key'].str.contains('other', case=False)
        ]
    print(filtered)

    # filters out disqualification message
    filtered = filtered[
        ~filtered['Key'].str.contains('disqualify', case=False)
        ]
    print(filtered)

    # added_columns = filter_valid_questions['Opt/Quest.'] = "Question"
    print("NO ERROR")
    print(filtered)

    cleaned_dataframe = {
        "QID": [],
        "Question": [],
        "Type": []
    }

    for index, row in filtered.iterrows():
        question_id = row['Key'].split("-")[1]
        cleaned_dataframe['QID'].append(question_id)

        question = row['Default Text']
        cleaned_dataframe['Question'].append(question)

        if "-o-" in row['Key']:
            cleaned_dataframe['Type'].append("option")
        else:
            cleaned_dataframe['Type'].append("question")

    cleaned_order = pd.DataFrame(cleaned_dataframe)
    cleaned_order.to_csv("testy_test.csv", encoding="utf-8-sig", index=False)

    print(cleaned_order.head(10))
