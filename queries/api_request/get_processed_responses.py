import pandas as pd


def process_responses(response_list):
    """
    checks which responses are valid, and
    """

    # filters out the responses that are not complete
    valid = [x for x in response_list['data'] if x['status'] == 'Complete']
    print(len(valid))

    # creating a matrix of question titles with
    # empty lists to receive answers
    question_answer_df = {}

    response_1 = valid[0]['survey_data']
    for key, value in response_1.items():
        id = key
        question = value['question']
        question_answer_df[f'{id} : {question}'] = []

    # Searches each response and appends each answer to
    # each question to the respective list in the matrix
    for response in valid:
        for key, value in response['survey_data'].items():
            if 'answer' in value:
                question_answer_df[
                    key + ' : ' + value['question']
                ].append(value['answer'])
            elif 'options' in value:
                question_answer_df[
                    key + ' : ' + value['question']
                ].append(value['options'])
            else:
                question_answer_df[
                    key + ' : ' + value['question']
                ].append('N/A')

    # Turn the matrix into a dataframe and output to csv
    data_frame = pd.DataFrame(question_answer_df)
    return question_answer_df
