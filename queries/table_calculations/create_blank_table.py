"""
Defines the create_blank_table function.

This function will add all the crossbreaks and questions
to a big table full of zeros ready to receive the total
number of respondents in each crossbreak who answered a
certain way.
"""

import pandas as pd
from . import define_standard_crossbreaks as cb

def create_blank_table(question_data):
    """
    Creates a table filled with zeros.

    The first column will be a list of questions/answers.
    The subsequent columns will be a total column
    and a column for each crossbreak.
    """
    questions = question_data

    # filters out entries that aren't 'Questions' or 'Options'.
    questions = questions[
        questions['question_text'].str.contains('Question|Option|sub_option|sub_question', na=False)
    ]

    table = {
        'IDs':["Total", "Weighted",],
        'Types': ["Total", "Weighted",],
        'Base Type': ["Total", "Weighted"],
        'Answers': ["Total", "Weighted",],
        'Rebase comment needed': ["Total", "Weighted",],
        'Total': [0, 0,],
        f'{cb.GENDER[0]}': [0, 0,],
        f'{cb.GENDER[1]}': [0, 0,],
        f'{cb.AGE[0]}': [0, 0,],
        f'{cb.AGE[1]}': [0, 0,],
        f'{cb.AGE[2]}': [0, 0,],
        f'{cb.AGE[3]}': [0, 0,],
        f'{cb.AGE[4]}': [0, 0,],
        f'{cb.AGE[5]}': [0, 0,],
        f'{cb.REGION[0]}': [0, 0,],
        f'{cb.REGION[1]}': [0, 0,],
        f'{cb.REGION[2]}': [0, 0,],
        f'{cb.REGION[3]}': [0, 0,],
        f'{cb.REGION[4]}': [0, 0,],
        f'{cb.REGION[5]}': [0, 0,],
        f'{cb.REGION[6]}': [0, 0,],
        f'{cb.REGION[7]}': [0, 0,],
        f'{cb.REGION[8]}': [0, 0,],
        f'{cb.REGION[9]}': [0, 0,],
        f'{cb.REGION[10]}': [0, 0,],
        f'{cb.REGION[11]}': [0, 0,],
    }

    for i in range(len(questions.index)):
        table['Answers'].append(
            f'{questions.iloc[i, 3]}'
        )

    for j in range(len(questions.index)):
        table['Rebase comment needed'].append(
            f'{questions.iloc[j, 4]}'
        )

    for j in range(len(questions.index)):
        table['Types'].append(
            f'{questions.iloc[j, 2]}'
        )

    for j in range(len(questions.index)):
        table['Base Type'].append(
            f'{questions.iloc[j, 1]}'
        )

    for j in range(len(questions.index)):
        table['IDs'].append(
            f'{questions.iloc[j, 0]}'
        )

    list_zeros = [0] * len(table['Answers'])
    protected_keys = [
        'Answers', 'IDs', 'Types', 'Rebase comment needed', 'Base Type']
    for key, value in table.items():
        if key not in protected_keys:
            table[key] = list_zeros

    dataframe = pd.DataFrame(table)
    dataframe.to_csv('blank_table.csv')
    print(dataframe.head(5))
    return dataframe
