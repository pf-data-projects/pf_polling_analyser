import pandas as pd


def process_responses():
    """
    checks which responses are valid, and
    """

    # filters out the responses that are not complete
    valid = [x for x in data['data'] if x['status'] == 'Complete']
    print(len(valid))

    # creating a matrix of question titles with
    # empty lists to receive answers
    question_answer_df = {}

    response_1 = valid[0]['survey_data']
    for key, value in response_1.items():
        id = key
        question = value['question']
        question_answer_df[f'{id} : {question}'] = []

    # workaround for some valid responses not having
    # question 180 displayed to them
    for i in valid:
        if "180" in i['survey_data']:
            continue
        else:
            i['survey_data']["180"] = {
                "answer": "N/A",
                "question": "You said that at least some of the money spent on the NHS is wasted.<br /><br />\nWhich of the following, if any, do you think of as ways the money spent on the NHS is wasted?<br /><br /><em>Select any which apply</em>",
            }

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
    data_frame.to_csv('survey_responses.csv', index=False, index_label=None)