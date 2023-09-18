"""
Creates a table filled with zeros.

The first column will be a list of questions/answers.
The subsequent columns will be a total column
and a column for each crossbreak.
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

    table = {
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
            f'{questions.iloc[i, 1]}: {questions.iloc[i, 4]}'
        )

    LIST_ZEROS = [0] * len(table['Answers'])

    for key in table.items():
        if key != 'Answers':
            table[key] = LIST_ZEROS

    dataframe = pd.DataFrame(table)
    print(dataframe.head(10))
    return dataframe
