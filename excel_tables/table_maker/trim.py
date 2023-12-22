"""
This file contains one function that carries out
a number of small processing tasks to the data before
it is exported to excel.

In future these could be split into multiple functions
that are handled by the view. This may aid readability/maintainability
in the longer term.

1. Add edited rebase comments to the 'answers' column of the table.
2. Add 'All respondents' as default to all other 'answers' records.
3. trim the data according to start and end specified by user.
4. remove unnecessary question types.
5. deletes any html tags present in questions.
6. add extra empty rows for excel readability.
"""

import pandas as pd

def trim_table(data, start, end, comments):
    """
    A function that:
    1. takes the start and end of the survey
    defined by the user and trims off the parts of the table that
    are not needed.
    2. removes other unnecessary rows of the table.
    """

    # remove any html tags from questions
    data["Answers"] = data["Answers"].str.replace(
        r'<[^>]+>',
        '',
        regex=True
    )

    grid_summaries = create_grid_summaries(data)
    rank_summaries = create_rank_summaries(data)

    summaries = grid_summaries[0] + rank_summaries[0]
    unique_ids = grid_summaries[1] + rank_summaries[1]

    # Add the edited rebase comments to the table.
    for comment in comments:
        filtered_df = data[data['IDs'] == str(comment[0])]
        filtered_df = filtered_df[filtered_df['Base Type'] == 'Question']
        updated_question = filtered_df['Answers'] + f" BASE: {comment[1]}"
        updated_question = pd.DataFrame(updated_question)
        data_row_index = data[
            (data['Base Type'] == "Question") & (data['IDs'] == str(comment[0]))
        ].index
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
        return False
        # raise ValueError("The specified IDs were not found in the CSV file.")

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
    questions = new_data['Base Type'] == 'Question'
    question_indexes = new_data[questions].index.tolist()
    adjusted_indexes = [index + 4 for index in question_indexes]
    adjusted_indexes.insert(0, '')

    # new_data.to_csv("test_output.csv", encoding="utf-8-sig", index=False)

    return [new_data, adjusted_indexes, summaries, unique_ids]

def create_grid_summaries(data):
    """
    This function:

    1. filters the dataframe by questions that have table
    or rank base type

    2. get a unique list of ids

    3. for each of these create a table by:
    - iterating through the sub-options
    - adding the totals data to to a new column in a new dataframe
    
    4. Each table saved in a list of tables that is returned by the
    main trim function.
    """

    # Get a list of IDs for table questions
    table_questions = data[data['Types'] == 'TABLE']
    # rank_questions = data[data['Types'] == 'RANK']
    table_ids = table_questions['IDs'].tolist()
    # rank_ids = rank_questions['IDs'].tolist()
    all_ids = table_ids # + rank_ids
    unique_ids = list(dict.fromkeys(all_ids))

    grids = []

    for qid in unique_ids:
        question = data[data['IDs'] == qid]

        identifier = 0
        within_sub_question = False

        # Create a new column for the identifier
        question['Identifier'] = None

        # Logic for adding mapping
        for index, row in question.iterrows():
            if row['Base Type'] == 'sub_Question':
                identifier += 1
                within_sub_question = True
            elif row['Base Type'] != 'sub_option':
                within_sub_question = False
            # Assign the identifier to 'sub_Question' and its 'sub_option' rows
            if within_sub_question:
                question.at[index, 'Identifier'] = identifier

        # get the question and options
        table_options =  question[question['Types'] == 'TABLE']
        # rank_options = question[question['Types'] == 'RANK']
        table_options_list = table_options['Answers'].tolist()
        # rank_options_list = rank_options['Answers'].tolist()
        options_list = table_options_list # + rank_options_list
        sliced = options_list[1:]
        grid = {
            f'{options_list[0]}': sliced,
        }

        all_identifiers = question['Identifier'].to_list()
        identifiers = list(dict.fromkeys(all_identifiers))

        for identifier in identifiers:
            if identifier is None:
                continue
            sub_question = question[question['Identifier'] == identifier]
            sub_options = sub_question['Total'].tolist()
            grid[sub_question.iloc[0, 3]] = sub_options[1:]

        grid_df = pd.DataFrame(grid)
        grids.append(grid_df)

    return [grids, unique_ids]

def create_rank_summaries(data):
    """
    A similar function for handling rank type questions.
    """
    rank_questions = data[data['Types'] == 'RANK']
    rank_ids = rank_questions['IDs'].tolist()
    unique_ids = list(dict.fromkeys(rank_ids))

    grids = []

    for qid in unique_ids:
        question = data[data['IDs'] == qid]

        identifier = 0
        within_sub_question = False

        # Create a new column for the identifier
        question['Identifier'] = None

        # Logic for adding mapping
        for index, row in question.iterrows():
            if row['Base Type'] == 'Option':
                identifier += 1
                within_sub_question = True
            elif row['Base Type'] != 'sub_option':
                within_sub_question = False
            # Assign the identifier to 'sub_Question' and its 'sub_option' rows
            if within_sub_question:
                question.at[index, 'Identifier'] = identifier

        # find the question text and all options.
        rank_question = question[question['Base Type'] == 'Question']
        rank_options = question[question['Base Type'] == 'sub_option']
        options_list = rank_options['Answers'].tolist()
        unique_options = list(dict.fromkeys(options_list))
        grid = {
            f'{rank_question.iloc[0, 3]}': unique_options,
        }

        all_identifiers = question['Identifier'].to_list()
        identifiers = list(dict.fromkeys(all_identifiers))

        for identifier in identifiers:
            if identifier is None:
                continue
            sub_question = question[question['Identifier'] == identifier]
            sub_options = sub_question['Total'].tolist()
            grid[sub_question.iloc[0, 3]] = sub_options[1:]

        grid_df = pd.DataFrame(grid)
        grids.append(grid_df)

    return [grids, unique_ids]
