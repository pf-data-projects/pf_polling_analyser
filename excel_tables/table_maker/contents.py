import pandas as pd

def create_contents_page(data):
    """
    Build a dataframe to house the contents page
    of PF polling tables.
    """
    data = data[(data['Base Type'] == "Question")]
    question_list = data['Answers'].tolist()
    print(len(question_list))
    # question_list = list(dict.fromkeys(question_list))
    print(len(question_list))

    id_list = data['IDs'].tolist()
    # id_list = list(dict.fromkeys(id_list))
    print(len(id_list))

    data.to_csv("test_output_2.csv", encoding="utf-8-sig", index=False)

    # create the df that will show individual tables/sheets
    contents_list = []
    contents_list.append('Full Results')
    for item in question_list:
        if item != 'Total' and item != 'Weighted':
            contents_list.append(item)
    contents = {"Table of Contents": contents_list}
    contents_df = pd.DataFrame(contents)

    return [contents_df, id_list]
