import io

import pandas as pd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from django.core.cache import cache

from .contents import create_contents_page
from .cover import create_cover_page
from .helper import get_column_letter

def create_workbook(request, data, title):
    """
    The function that controls the creation and formatting of
    polling tables.
    """
    # create a further trimmed dataframe for excel output
    trimmed_data = data.drop(
        ['IDs', 'Types', 'Base Type', 'Rebase comment needed'],
        axis=1
    )

    # create cover page and contents page
    # blank = {'Table of contents'}
    cover_df = create_cover_page(data)
    contents_df = create_contents_page(data)

    # define variables for caching
    cache_key = "tables_for_user_" + str(request.user.id)
    output = io.BytesIO()

    # Format the tables with xlsxwriter and pandas
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create main results polling table
        cover_df.to_excel(writer, index=False, sheet_name="Cover Page")
        contents_df[0].to_excel(writer, index=False, sheet_name="Contents")
        trimmed_data.to_excel(writer, index=False, sheet_name='Full Results')
        workbook = writer.book
        results_sheet = writer.sheets['Full Results']
        contents_sheet = writer.sheets['Contents']

        # add link to the full results page in the contents page
        position = contents_df[0].isin(['Full Results']).stack()
        if not position.empty:
            # Get the first match's index
            first_match_index = position[position].index[0]

            # Get row and column for the DataFrame
            df_row = first_match_index[0]
            df_col = first_match_index[1]

            # Convert the DataFrame column label to an Excel column letter
            excel_col = get_column_letter(contents_df[0].columns.get_loc(df_col) + 1)
            excel_row = df_row + 2  # Adding 1 because Excel starts at 1
            excel_cell = f"{excel_col}{excel_row}"
            contents_sheet.write_url(
                excel_cell,
                "internal:'Full Results'!A1",
                string="Full Results Table"
            )
        else:
            print("Value 'Full Results' not found in DataFrame.")

        results_sheet.set_zoom(90)
        header_format = workbook.add_format({
            "bg_color": "#FFA500",
            "bold": True,
            "font_color": "#FFFFFF"
        })
        percent_format = workbook.add_format({'num_format': '0%'})
        question_format = workbook.add_format({"bold": True})
        # Apply a general format to the entire column
        # without the percentage format
        results_sheet.set_column(5, len(data.columns) - 1, 15)

        # create question style and loop to apply them
        for i in range(2, len(data)):
            question_value = data.iloc[i, 3]
            if data.at[i, 'Base Type'] == 'Question' or data.at[i, 'Base Type'] == 'sub_Question':
                results_sheet.write(i + 1, 0, question_value, question_format)
                results_sheet.merge_range(i + 1, 0, i + 1, 26, question_value, question_format)

        # apply percentage format to data.
        format_percentages(trimmed_data, results_sheet, percent_format)

        for col_num, value in enumerate(trimmed_data.columns.values):
            results_sheet.write(0, col_num, value, header_format)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create individual tables
        non_header_data = data.iloc[2:]
        header = data.loc[0:1]
        ids = non_header_data['IDs'].tolist()
        checked = []
        for qid in ids:
            if qid not in checked:
                sub_table = data[(data['IDs'] == qid)]
                rows_list = []
                for index, row in sub_table.iterrows():
                    if row['Base Type'] in ['Question']:
                        empty_row = pd.Series([''] * len(data.columns), index=data.columns)
                        rows_list.append(empty_row)
                    rows_list.append(row)
                sub_table = pd.concat([pd.DataFrame([row]) for row in rows_list], ignore_index=True)
                sub_table.reset_index(drop=True, inplace=True)
                concat_sub_table = pd.concat(
                    [header, sub_table],
                    ignore_index=True
                )
                sub_table.reset_index(drop=True, inplace=True)
                concat_sub_table = concat_sub_table.drop(
                    ['IDs', 'Types', 'Base Type', 'Rebase comment needed'],
                    axis=1
                )
                new_row = {concat_sub_table.columns[0]: 'Back to contents'}
                for col in concat_sub_table.columns[1:]:
                    new_row[col] = ''
                concat_sub_table.loc[len(concat_sub_table)] = new_row
                concat_sub_table.to_excel(
                    writer,
                    index=False,
                    sheet_name=f'question ID - {qid}'
                )
                question_sheet = writer.sheets[f'question ID - {qid}']
                # format numbers to nice percentages
                format_percentages(
                    concat_sub_table, question_sheet, percent_format
                )
                # format questions
                for i in range(len(sub_table)):
                    question_value = concat_sub_table.iloc[i + 2, 0]
                    if sub_table.loc[i, 'Base Type'] == 'Question' or sub_table.loc[i, 'Base Type'] == 'sub_Question':
                        question_sheet.write(
                            i + 3,
                            0,
                            question_value,
                            question_format
                        )
                        question_sheet.merge_range(i + 3, 0, i + 3, 25, question_value, question_format)
                # format headers
                for col_num, value in enumerate(concat_sub_table.columns.values):
                    question_sheet.write(0, col_num, value, header_format)
                # add link back to contents
                position = concat_sub_table.isin(['Back to contents']).stack()
                if not position.empty:
                    first_match_index = position[position].index[0]

                    df_row = first_match_index[0]
                    df_col = first_match_index[1]

                    excel_col = get_column_letter(concat_sub_table.columns.get_loc(df_col) + 1)
                    excel_row = df_row + 2
                    excel_cell = f"{excel_col}{excel_row}"
                    question_sheet.write_url(
                        excel_cell,
                        "internal:'Contents'!A1",
                        string="Back to Contents"
                    )
            checked.append(qid)

        # Once tables are made, create links to each from contents page.
        question_id_list = contents_df[1]
        i = 0
        for question in question_id_list:
            df_row = i + 1
            df_col = 0
            if i < len(contents_df[0]):
                cell_data = contents_df[0].iat[i + 1, 0]
                excel_col = "A"
                excel_row = df_row + 2
                excel_cell = f"{excel_col}{excel_row}"
                contents_sheet.write_url(
                    excel_cell,
                    f"internal:'question ID - {question}'!A1",
                    string=f'{cell_data}'
                )
            i += 1

    output.seek(0)
    cache.set(cache_key, output.getvalue(), timeout=300)
    return cache_key


def format_percentages(data, sheet, cell_format):
    """
    # Loop through rows, starting from the fourth row, 
    # and apply the percentage format
    """
    for row_num in range(3, len(data)):  # start from the fourth row (index 3)
        row_data = data.iloc[row_num]
        for col_num in range(1, len(data.columns)):
            cell_value = data.iloc[row_num, col_num]
            # Check if the cell contains a number (int or float)
            if isinstance(cell_value, (int, float)):
                # Apply percent format to the cell because it contains a number
                sheet.write_number(row_num + 1, col_num, cell_value, cell_format)
            elif pd.isna(cell_value) or cell_value == '':
                # If the cell is NaN or an empty string, write an empty string
                sheet.write_string(row_num + 1, col_num, '')
            else:
                # Otherwise, write the value as it is (this covers non-empty strings)
                sheet.write(row_num + 1, col_num, cell_value)
