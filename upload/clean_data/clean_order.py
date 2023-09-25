import pandas as pd

def clean_order(order):
    """
    Takes the order dataframe as an argument and
    returns a cleaned version with just the question ids
    and questions/answers
    """
    filtered = order[order['Key'].str.contains('q-')]
    # added_columns = filter_valid_questions['Opt/Quest.'] = "Question"

    cleaned_dataframe = {
        "QID": [],
        "Question": [],
        "Type": []
    }

    for index, row in filtered.iterrows():
        question_id = row['Key'].split("-")[1]
        print(question_id)
        cleaned_dataframe['QID'].append(question_id)

        question = row['Default Text']
        cleaned_dataframe['Question'].append(question)

        if "-o-" in row['Key']:
            cleaned_dataframe['Type'].append("option")
        else:
            cleaned_dataframe['Type'].append("question")

    cleaned_order = pd.DataFrame(cleaned_dataframe)

    print(cleaned_order.head(50))
