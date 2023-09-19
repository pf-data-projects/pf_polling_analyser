"""
Defines the create_blank_table function.

This function will add all the crossbreaks and questions
to a big table full of zeros ready to receive the total
number of respondents in each crossbreak who answered a
certain way.
"""

import pandas as pd
import define_standard_crossbreaks as cb

def create_blank_table():
    """
    Creates a table filled with zeros.

    The first column will be a list of questions/answers.
    The subsequent columns will be a total column
    and a column for each crossbreak.
    """
    questions = pd.read_csv('question_data.csv')

    # filters out entries that aren't 'Questions' or 'Options'.
    questions = questions[
        questions['question_text'].str.contains('Question|Option', na=False)
    ]

    table = {
        'IDs':[],
        'Answers': [],
        'Total': [],
        f'{cb.GENDER[0]}': [],
        f'{cb.GENDER[1]}': [],
        f'{cb.AGE[0]}': [],
        f'{cb.AGE[1]}': [],
        f'{cb.AGE[2]}': [],
        f'{cb.AGE[3]}': [],
        f'{cb.AGE[4]}': [],
        f'{cb.AGE[5]}': [],
        f'{cb.REGION[0]}': [],
        f'{cb.REGION[1]}': [],
        f'{cb.REGION[2]}': [],
        f'{cb.REGION[3]}': [],
        f'{cb.REGION[4]}': [],
        f'{cb.REGION[5]}': [],
        f'{cb.REGION[6]}': [],
        f'{cb.REGION[7]}': [],
        f'{cb.REGION[8]}': [],
        f'{cb.REGION[9]}': [],
        f'{cb.REGION[10]}': [],
        f'{cb.REGION[11]}': [],
    }

    for i in range(len(questions.index)-1):
        table['Answers'].append(
            f'{questions.iloc[i, 4]}'
        )

    for j in range(len(questions.index)-1):
        table['IDs'].append(
            f'{questions.iloc[j, 1]}'
        )

    list_zeros = [0] * len(table['Answers'])
    for key, value in table.items():
        if key != 'Answers' and key != 'IDs':
            table[key] = list_zeros

    dataframe = pd.DataFrame(table)
    dataframe.to_csv('blank_table.csv', encoding='utf-8-sig', index=False)
    return dataframe
