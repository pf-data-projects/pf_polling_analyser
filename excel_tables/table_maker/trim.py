import pandas as pd

def trim_table(data, start, end):
    """
    A function that:
    1. takes the start and end of the survey
    defined by the user and trims off the parts of the table that
    are not needed.
    2. removes other unnecessary rows of the table.
    """
    # Find the index for the first row with the start_id
    start_index = data[data['IDs'] == str(start)].index.min()

    # Find the index for the last row with the end_id
    end_index = data[data['IDs'] == str(end)].index.max()

    # Check if both indices are found
    if pd.isna(start_index) or pd.isna(end_index):
        raise ValueError("The specified IDs were not found in the CSV file.")

    # Trim the DataFrame to only include rows between the found indices
    trimmed_data = data.loc[start_index:end_index]

    # remove textbox/essay/maxdiff questions
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'TEXTBOX']
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'ESSAY']
    trimmed_data = trimmed_data[trimmed_data['Types'] != 'MAXDIFF']

    # remove superfluous table options
    condition = (trimmed_data['Types'] == 'TABLE') & (trimmed_data['Base Type'] == 'Option')
    trimmed_data = trimmed_data[~condition]

    trimmed_data.reset_index(drop=True, inplace=True)

    trimmed_data.to_csv("test_output.csv", encoding="utf-8-sig", index=False)

    return trimmed_data
