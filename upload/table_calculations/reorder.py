"""
This module contains a function sort_answers to
check each question to see if it has randomised answers
in Alchemer. It then reorders the answers in these questions
based on the highest proportion of respondents in the totals
column.
"""

import pandas as pd

def sort_answers(df):
    """
    reorders answers for certain questions
    based on the number of respondents for each
    answer.
    """
    question_ids = df['IDs'].unique()
    print(df.dtypes)

    sorted_df_list = []

    for qid in question_ids:
        # Filter the dataframe for the current question ID
        qid_df = df[df['IDs'] == qid]
        # print(qid_df)

        # Check if the question has the value 'TRUE' in the 'Randomised' column
        if qid_df['Randomised'].iloc[0] == 'True':
            print("The statement is true")
            # Separate "Question" rows to keep them at the top
            question_rows = qid_df[(qid_df['Base Type'] == 'Question')]
            other_rows = qid_df[(qid_df['Base Type'] != 'Question')]

            # Sort the other rows by Total column in descending order
            sorted_other_rows = other_rows.sort_values(by='Total', ascending=False)

            # Ensure "None of the above" and "Don't know" are at the bottom
            none_above = sorted_other_rows[sorted_other_rows['Answers'] == 'None of the above']
            dont_know = sorted_other_rows[sorted_other_rows['Answers'] == "Don't know"]

            # Filter out "None of the above" and "Don't know" from the main sorted dataframe
            sorted_other_rows = sorted_other_rows[~sorted_other_rows['Answers'].isin(
                ['None of the above', "Don't know"])]

            # Append "None of the above" and "Don't know" back at the bottom
            sorted_other_rows = pd.concat([sorted_other_rows, none_above, dont_know])

            # Concatenate the question rows at the top with the sorted other rows
            sorted_qid_df = pd.concat([question_rows, sorted_other_rows])

            # Append to the list of sorted dataframes
            sorted_df_list.append(sorted_qid_df)
        else:
            # If not Randomised, append the original dataframe slice
            sorted_df_list.append(qid_df)

    # Concatenate all sorted dataframes
    sorted_df = pd.concat(sorted_df_list)

    return sorted_df.reset_index(drop=True)
