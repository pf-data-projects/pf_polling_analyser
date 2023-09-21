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
    print("Valid responses:", len(valid))

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
        question_id = key
        question = value[0]['question']
        question_answer_df[f'{question_id} : {question}'] = []

    # Searches each response and appends each answer to
    # each question to the respective list in the matrix
    # i = 1
    for key, value in aggregated_responses.items():
        for response in valid:
            # print("respondent:", i)
            if key in response['survey_data']:
                if response['survey_data'][key]['type'] == "ESSAY":
                    continue
                if 'answer' in response['survey_data'][key]:
                    question_answer_df[
                        key + ' : ' + value[0]['question']
                    ].append(response['survey_data'][key]['answer'])
                elif 'options' in response['survey_data'][key]:
                    question_answer_df[
                        key + ' : ' + value[0]['question']
                    ].append(response['survey_data'][key]['options'])
                elif 'shown' in response['survey_data'][key]:
                    shown = response['survey_data'][key]['shown']
                    if shown is False:
                        question_answer_df[
                            key + ' : ' + value[0]['question']
                        ].append('Not answered by respondent')
                    # extra condition if shown is true and there is no answer for question.
                    elif shown is True and 'answer' not in response['survey_data'][key]:
                        question_answer_df[
                            key + ' : ' + value[0]['question']
                        ].append('N/A')
                else:
                    question_answer_df[
                        key + ' : ' + value[0]['question']
                    ].append('N/A')
            else:
                question_answer_df[
                    key + ' : ' + value[0]['question']
                ].append('N/A')
            # print(len(question_answer_df["208 : What is the maximum you would be willing to pay for your ideal private number plate?"]))
            # print(len(question_answer_df["207 : At present, personalized (private) licence plates on vehicles have to match the style of non-personalised plates on vehicles. For example, the current format of two letters, two numbers a space and three letters - AB18 ABC. Or the older \u201cprefix\u201d format of A123 ABC.<br /><br />\nSuppose the government changed the rules to allow you to have any licence plate you like \u2013 for example your name, a love one\u2019s name, the name of your business or your job. How much more likely would you be to purchase a personalised number plate?"]))
            # i += 1


    question_answer_df = {
        k: v for k, v in question_answer_df.items() if len(v) != 0
        }
    # for key, value in question_answer_df.items():
    #     print(len(value), key)
    # Turn the matrix into a dataframe and output to csv
    data_frame = pd.DataFrame(question_answer_df)
    # print(data_frame.head(10))
    # data_frame.to_csv('response_data.csv', encoding='utf-8-sig')
    return data_frame

# process_responses(response_list)
