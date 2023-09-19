import pandas as pd

import define_standard_crossbreaks as cb

results = pd.read_csv('response_data.csv')
table = pd.read_csv('totals_calculated.csv')
question_data = pd.read_csv('question_data.csv')

questions = table['Answers'].tolist()
question_ids = table['IDs'].tolist()

question_list = []
for i in range(len(questions)):
    item = {
        'qid': f'{question_ids[i]}',
        'question': questions[i]
    }
    question_list.append(item)



# filtered_df = results[cb.columns_with_substring_question(results, gender_q)]
# get_gender = results[cb.columns_with_substring_question(results, gender_q)]
# filtered_df = results.loc[(results[get_gender.columns[0]] == 'Female')]
# filtered_df = filtered_df[cb.columns_with_substring(results, question_list[81]['qid'])]
# print(len(filtered_df.index))
# print(filtered_df)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ work out how males answered the survey


def calc_gender(category, col_index):
    """
    A function to run table calculations
    for gender crossbreaks.
    """
    gender_q = 'Which of the following best describes how you think of yourself?'
    for question in question_list:
        get_gender = results[cb.columns_with_substring_question(results, gender_q)]
        filtered_df = results.loc[(results[get_gender.columns[0]] == category)]
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
                        table['IDs'] == int(question['qid'])
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
    print(table.head(20))
    table.to_csv('gender.csv', encoding="utf-8-sig", index=False)
    print(category, "done!")

calc_gender("Male", 3)
calc_gender("Female", 4)
