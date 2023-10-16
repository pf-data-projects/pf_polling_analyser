import pandas as pd
from .create_blank_table import create_blank_table
from .define_standard_crossbreaks import (
    columns_with_substring, columns_with_substring_question)
from .gender import calc_gender
from .age import iterate_age_brackets
from .region import iterate_regions

# results = pd.read_csv('DEFINITELY-A-TEST.csv')
# question_data = pd.read_csv('question_data.csv')

def table_calculation(results, question_data):
    """
    A function that controls the flow of logic for the
    creation of the table.
    """
    # print(question_data.head(10))

    table = create_blank_table(question_data)
    questions = table['Answers'].tolist()
    question_ids = table['IDs'].tolist()
    question_types = table['Types'].tolist()
    question_rebase = table['Rebase comment needed'].tolist()

    question_list = []
    for i in range(len(questions)):
        item = {
            'qid': f'{question_ids[i]}',
            'question': questions[i],
            'type': question_types[i],
            'rebase': question_rebase[i],
        }
        question_list.append(item)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work out the totals for each question

    # loops through all question options to find
    # number of respondents who answered a certain way
    for question in question_list:
        # adds the total respondents to table
        table.iat[0, 5] = len(results.index)
        # finds column that contains question id
        filtered_df = results[columns_with_substring(results, question['qid'])]

        if filtered_df.shape[1] < 1:
            print(filtered_df)
            print("______________________")
            print(question["qid"])

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # IDEA FOR MULTI-SELECTS / TABLE QUESTIONS:
        # - checks to see if the filtered_df has more than one col
        # (if statement just below this changes to check empty AND one col size) -> This doesn't work... I need to understand how this is actually working...
        # - for each of the multiselect columns, check which substring exists in title
        # - check how many of each option features in each col
        # - maybe just use all options related to the QID but filter out duplicates?
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # checks that question exists in responses.
        if not filtered_df.empty:
            all_options = question_data.loc[
                (question_data['question_text'] == 'Option')
                ]
            relevant_options = all_options.loc[
                (all_options['question_id'] == int(question['qid']))
            ]
            if len(relevant_options.index) == 0:
                relevant_options = all_options.loc[
                    (all_options['question_id'] == question['qid'])
                ]
            options = relevant_options['question_title'].tolist()
            # checks that there are options for the question.
            # E.G. Age crossbreak question has no options.
            if len(options) > 0:
                for i, option in enumerate(options):
                    second_filtered_df = filtered_df[
                        filtered_df.iloc[:, 0] == options[i]
                        ]
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
                        table.iat[position_int, 5] = len(second_filtered_df.index)
                    else:
                        continue
            else:
                continue
        else:
            continue
    print(table)
    print("---- PROCESSING GENDER CROSSBREAKS ----")
    table = calc_gender("Male", 6, table, question_list, results, question_data)
    table = calc_gender("Female", 7, table, question_list, results, question_data)
    print("---- PROCESSING AGE CROSSBREAKS ----")
    table = iterate_age_brackets(table, question_list, results, question_data)
    print("---- PROCESSING REGION CROSSBREAKS ----")
    table = iterate_regions(table, question_list, results, question_data)

    # create a csv for manual QA
    # table.to_csv('totals_calculated.csv', encoding="utf-8-sig", index=False)
    print("table created")
    # Display all values as a percentage of the total for each crossbreak.
    first_row_values = table.iloc[0, 5:]
    table.iloc[1:, 5:] = table.iloc[1:, 5:].div(first_row_values) * 100
    return table
