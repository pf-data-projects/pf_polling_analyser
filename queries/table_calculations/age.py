import pandas as pd

from . import define_standard_crossbreaks as cb

def calc_age(category, col_index, table, question_list, results, question_data):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    age_q = 'How old are you?'
    for question in question_list:
        get_age = results[cb.columns_with_substring_question(results, age_q)]
        filtered_df = results.loc[
            (results[get_age.columns[0]] >= category[0])
            ]
        filtered_df = filtered_df.loc[(results[get_age.columns[0]] <= category[1])]
        filtered_df = filtered_df[cb.columns_with_substring(results, question['qid'])]
        # checks that question exists in responses.
        if not filtered_df.empty:
            all_options = question_data.loc[(question_data['question_text'] == 'Option')]
            relevant_options = all_options.loc[
                (all_options['question_id'] == int(question['qid']))
            ]
            options = relevant_options['question_title'].tolist()
            # checks that there are options for the question.
            # E.G. Age crossbreak question has no options.
            if len(options) > 0:
                for i, option in enumerate(options):
                    second_filtered_df = filtered_df[filtered_df.iloc[:, 0] == options[i]]
                    position = table[(
                        table['Answers'] == options[i]
                    ) & (
                        table['IDs'] == question['qid']
                    )].index

                    # Checks that this exists in the table.
                    # I think the different indexers for
                    # different loops are not quite the same.
                    if len(position) > 0:
                        position_int = int(position[0])
                        table.iat[position_int, col_index] = len(second_filtered_df.index)
                    else:
                        continue
            else:
                continue
        else:
            continue
    # print(table.head(20))
    # table.to_csv('age.csv', encoding="utf-8-sig", index=False)
    print(category[0], "done!")
    return table


def iterate_age_brackets(table, question_list, results, question_data):
    """ 
    Builds a list of age brackets from the cb module
    and calls the calc_age func based on the data
    in the list of age bracket objects.
    """
    ages = cb.AGE
    table_col = 5
    age_brackets = []
    for age in ages:
        if "-" in age:
            num1 = int(age.split("-", 1)[0])
            num2 = int(age.split("-", 1)[1])
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        else:
            num1 = int(age.split("+", 1)[0])
            num2 = 200
            bracket = {
                'num1': num1,
                'num2': num2,
                'col': table_col
            }
            age_brackets.append(bracket)
        table_col += 1
    for bracket in age_brackets:
        table = calc_age(
            [bracket['num1'], bracket['num2']],
            bracket['col'],
            table,
            question_list,
            results,
            question_data
        )
        # print(table)
    return table
