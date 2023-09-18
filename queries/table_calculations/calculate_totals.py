import pandas as pd
from create_blank_table import create_blank_table


results = pd.read_csv('response_data.csv')
question_data = pd.read_csv('question_data.csv')
questions_only = question_data.loc[
    question_data['question_text'] == 'Question'
]
question_iterator = results.columns.tolist()

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

def columns_with_substring(df, substring):
    """
    Small helper function that returns the column
    of a dataframe that contains a specified substring.
    """
    return [
        col for col in df.columns if col.split(" : ", 1)[0] == substring
        ]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Work out the totals for each question

for question in question_list:
    filtered_df = results[columns_with_substring(results, question['qid'])]
    all_options = question_data.loc[(question_data['question_text'] == 'Option')]
    relevant_options = all_options.loc[
        (all_options['question_id'] == int(question_list[81]['qid']))
        ]
    print(relevant_options)
