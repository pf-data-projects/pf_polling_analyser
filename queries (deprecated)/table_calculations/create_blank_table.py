"""
Defines the create_blank_table function.

This function will add all the crossbreaks and questions
to a big table full of zeros ready to receive the total
number of respondents in each crossbreak who answered a
certain way.
"""

import pandas as pd
from . import define_standard_crossbreaks as cb

def create_blank_table(question_data, standard_cb, non_standard_cb):
    """
    Creates a table filled with zeros.

    The first column will be a list of questions/answers.
    The subsequent columns will be a total column
    and a column for each crossbreak.
    """
    questions = question_data

    # filters out entries that aren't 'Questions' or 'Options'.
    questions = questions[
        questions['question_text'].str.contains('Question|Option|sub', na=False)
    ]

    table = {
        'IDs':["Total", "Weighted",],
        'Types': ["Total", "Weighted",],
        'Base Type': ["Total", "Weighted"],
        'Answers': ["Total", "Weighted",],
        'Rebase comment needed': ["Total", "Weighted",],
        'Total': [0, 0,],
    }

    for crossbreak in standard_cb:
        if crossbreak in cb.CROSSBREAKS:
            # condition to ensure voting intention cols don't overwrite 2019 cols
            if crossbreak == "voting_intention":
                for i in cb.CROSSBREAKS[crossbreak]:
                    table[f'intention_{i}'] = [0, 0,]
                table[f"blank_{crossbreak}"] = " "
            # condition to ensure brexit vote cols don't overwrite 2019 cols
            if crossbreak == "eu2016":
                for i in cb.CROSSBREAKS[crossbreak]:
                    table[f'brexit_{i}'] = [0, 0,]
                table[f"blank_{crossbreak}"] = " "
            else:
                for i in cb.CROSSBREAKS[crossbreak]:
                    table[i] = [0, 0,]
                table[f"blank_{crossbreak}"] = " "

    if len(non_standard_cb) > 0:
        for crossbreak in non_standard_cb:
            for answer in crossbreak[2]:
                table[f'{crossbreak[0]}: {answer}'] = [0, 0,]
            table[f"blank_{crossbreak[1]}_{crossbreak[2]}"] = " "

    for j in range(len(questions.index)):
        table['Answers'].append(
            f'{questions.iloc[j, 3]}'
        )
        table['Rebase comment needed'].append(
            f'{questions.iloc[j, 4]}'
        )
        table['Types'].append(
            f'{questions.iloc[j, 2]}'
        )
        table['Base Type'].append(
            f'{questions.iloc[j, 1]}'
        )
        table['IDs'].append(
            f'{questions.iloc[j, 0]}'
        )

    list_zeros = [0] * len(table['Answers'])
    protected_keys = [
        'Answers', 'IDs', 'Types', 'Rebase comment needed', 'Base Type'
    ]
    for key, value in table.items():
        if key not in protected_keys:
            table[key] = list_zeros

    dataframe = pd.DataFrame(table)

    for col in dataframe.columns:
        if 'blank_' in col:
            dataframe = dataframe.rename(columns={col: ' '})

    dataframe['Answers'] = dataframe['Answers'].str.strip()

    dataframe.to_csv('blank_table.csv')
    return dataframe
