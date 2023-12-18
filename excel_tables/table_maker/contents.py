"""
This file handles the creation of the contents page
which will be appended to the start of the excel tables.
"""

import pandas as pd

def create_contents_page(data, questions_list, comments, grids, unique_ids):
    """
    Build a dataframe to house the contents page
    of PF polling tables.
    """
    data = data[(data['Base Type'] == "Question")]
    question_list = data['Answers'].tolist()
    # question_list = list(dict.fromkeys(question_list))

    id_list = data['IDs'].tolist()
    # id_list = list(dict.fromkeys(id_list))

    # data.to_csv("test_output_2.csv", encoding="utf-8-sig", index=False)

    # create the df that will show individual tables/sheets
    contents_list = []
    contents_list.append('Full Results')
    for item in question_list:
        if item != 'Total' and item != 'Weighted':
            contents_list.append(item)
    id_column = []
    grid_indexes = []
    id_column.append(' ')
    for item in id_list:
        if item in unique_ids:
            id_column.append(item)
            grid_indexes.append(len(id_column) - 1)
        if item != 'Total' and item != 'Weighted':
            id_column.append(item)

    # print(grid_indexes)

    for item in grid_indexes:
        contents_list.insert(int(item), f"Grid Summary - {id_column[int(item)]}")
        questions_list.insert(int(item), "n/a")

    # print(len(contents_list))
    # print(len(id_column))
    # print(len(questions_list))

    contents = {
        "Question": contents_list, 
        'ID': id_column,
        'Row in Full Results': questions_list,
    }
    contents_df = pd.DataFrame(contents)
    contents_df["Number"] = range(1, len(contents_df) + 1)
    column_order = ["Number"] + ["ID"] + ["Question"] + ['Row in Full Results']
    contents_df = contents_df[column_order]
    contents_df["Base"] = "All Respondents"

    for comment in comments:
        contents_df_index = contents_df[contents_df['ID'] == str(comment[0])].index
        if not contents_df_index.empty:
            contents_df.iat[contents_df_index[0], 3] = comment[1]

    return [contents_df, id_column]
