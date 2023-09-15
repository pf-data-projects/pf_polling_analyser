import json
import pandas as pd

with open('response_list.json', 'r') as f:
    response_list = json.load(f)

def process_responses(response_list):
    """
    checks which responses are valid, and
    """
    with open('response_list.json', 'w') as f:
        json.dump(response_list, f, indent=2)

    # filters out the responses that are not complete
    valid = [x for x in response_list['data'] if x['status'] == 'Complete']
    print(len(valid))

    # get a dictionary that has all the responses
    # needed to form an empty table.
    aggregated_responses = {}
    for j in valid:
        for key in j['survey_data']:
            if key not in aggregated_responses:
                aggregated_responses[key] = []
            aggregated_responses[key].append(j['survey_data'][key])

    # creating a matrix of question titles with
    # empty lists to receive answers
    question_answer_df = {}

    for key, value in aggregated_responses.items():
        id = key
        question = value[0]['question']
        question_answer_df[f'{id} : {question}'] = []

    # Searches each response and appends each answer to
    # each question to the respective list in the matrix
    for key, value in aggregated_responses.items():
        for response in valid:
            if key in response['survey_data']:
                try:
                    if response['survey_data'][key]['answer']:
                        question_answer_df[
                            key + ' : ' + value[0]['question']
                        ].append(response['survey_data'][key]['answer'])
                    elif response['survey_data'][key]['options']:
                        print(False)
                        question_answer_df[
                            key + ' : ' + value[0]['question']
                        ].append(response['survey_data'][key]['options'])
                except KeyError:
                    # print(f'{key} exception')
                    question_answer_df[
                        key + ' : ' + value[0]['question']
                    ].append('N/A')
            else:
                question_answer_df[
                    key + ' : ' + value[0]['question']
                ].append('N/A')

    # Turn the matrix into a dataframe and output to csv
    data_frame = pd.DataFrame(question_answer_df)
    print(data_frame.head(10))
    data_frame.to_csv('response_data.csv', encoding='utf-8-sig')
    return data_frame

# process_responses(response_list)
