import pandas as pd

def trim_table(data, start, end, comments):
    """
    A function that:
    1. takes the start and end of the survey
    defined by the user and trims off the parts of the table that
    are not needed.
    2. removes other unnecessary rows of the table.
    """
    # Add the edited rebase comments to the table.
    for comment in comments:
        filtered_df = data[data['IDs'] == str(comment[0])]
        filtered_df = filtered_df[filtered_df['Base Type'] == 'Question']
        updated_question = filtered_df['Answers'] + f" BASE: {comment[1]}"
        updated_question = pd.DataFrame(updated_question)
        data_row_index = data[(data['Base Type'] == "Question") & (data['IDs'] == str(comment[0]))].index
        if not data_row_index.empty:
            data.iat[data_row_index[0], 3] = updated_question.iat[0, 0]

    # Add 'BASE: All respondents' to all other questions
    comment_ids = []
    for comment in comments:
        comment_ids.append(str(comment[0]))

    filtered_df = data[~data['IDs'].isin(comment_ids)]
    for index, row in filtered_df.iterrows():
        if row['Base Type'] == 'Question':
            updated = row['Answers'] + " BASE: All respondents"
            data.iat[index, 3] = updated
    data.to_csv("test_rebase.csv", index=False)

    # Find the index for the first row with the start_id
    start_index = data[data['IDs'] == str(start)].index.min()

    # Find the index for the last row with the end_id
    end_index = data[data['IDs'] == str(end)].index.max()

    # Check if both indices are found
    if pd.isna(start_index) or pd.isna(end_index):
        raise ValueError("The specified IDs were not found in the CSV file.")

    # Save the totals/weighted totals
    headers = data.loc[0:1]

    # Trim the DataFrame to only include rows between the found indices
    trimmed_data = data.loc[start_index:end_index]

    # remove textbox/essay/maxdiff questions
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'TEXTBOX']
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'ESSAY']
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'MAXDIFF']

    # divide all values by 100
    trimmed_data.iloc[:, 5:] = trimmed_data.iloc[:, 5:].applymap(
        lambda x: x / 100 if x != 0 else x
    )

    # remove superfluous table options
    condition = (trimmed_data['Types'] == 'TABLE') & (trimmed_data['Base Type'] == 'Option')
    trimmed_data = trimmed_data[~condition]

    # replace zeros from question and subquestion rows with empty strings
    question_rows = ['Question', 'sub_Question']
    condition = trimmed_data['Base Type'].isin(question_rows)
    trimmed_data.loc[condition] = trimmed_data.loc[condition].replace(0, '')

    trimmed_data.reset_index(drop=True, inplace=True)
    concatenated_data = pd.concat([headers, trimmed_data], ignore_index=True)
    concatenated_data.reset_index(drop=True, inplace=True)

    # remove any html tags from questions
    concatenated_data["Answers"] = concatenated_data["Answers"].str.replace(
        r'<[^>]+>',
        '',
        regex=True
    )

    # Create a list to store the rows
    rows_list = []

    # Iterate through the DataFrame and insert rows
    # with empty strings before 'Question' or 'sub_Question'
    for index, row in concatenated_data.iterrows():
        if row['Base Type'] in ['Question']:
            # Create a Series with empty strings for each column
            empty_row = pd.Series([''] * len(data.columns), index=data.columns)
            rows_list.append(empty_row)

        # Add the original row to the list
        rows_list.append(row)

    # Concatenate the list into a new DataFrame
    new_data = pd.concat([pd.DataFrame([row]) for row in rows_list], ignore_index=True)

    # Reset the index of the new DataFrame
    new_data.reset_index(drop=True, inplace=True)

    new_data.to_csv("test_output.csv", encoding="utf-8-sig", index=False)

    return new_data
