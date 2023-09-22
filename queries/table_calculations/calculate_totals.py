import pandas as pd
from create_blank_table import create_blank_table
from define_standard_crossbreaks import columns_with_substring, columns_with_substring_question
from gender import calc_gender
from age import iterate_age_brackets
from region import iterate_regions


results = pd.read_csv('DEFINITELY-A-TEST.csv')
question_data = pd.read_csv('question_data.csv')

table = create_blank_table()
questions = table['Answers'].tolist()
question_ids = table['IDs'].tolist()

question_list = []
for i in range(len(questions)):
    item = {
        'qid': f'{question_ids[i]}',
        'question': questions[i]
    }
    question_list.append(item)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work out the totals for each question

# loops through all question options to find
# number of respondents who answered a certain way
for question in question_list:
    filtered_df = results[columns_with_substring(results, question['qid'])]
    # checks that question exists in responses.
    if not filtered_df.empty:
        all_options = question_data.loc[
            (question_data['question_text'] == 'Option')
            ]
        relevant_options = all_options.loc[
            (all_options['question_id'] == int(question['qid']))
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
                    table.iat[position_int, 2] = len(second_filtered_df.index)
                else:
                    continue
        else:
            continue
    else:
        continue

print("OK")
table = calc_gender("Male", 3, table, question_list, results, question_data)
table = calc_gender("Female", 4, table, question_list, results, question_data)
table = iterate_age_brackets(table, question_list, results, question_data)
table = iterate_regions(table, question_list, results, question_data)

total_respondents = len(table.index)
constant = 1 / total_respondents


table.to_csv('totals_calculated.csv', encoding="utf-8-sig", index=False)
