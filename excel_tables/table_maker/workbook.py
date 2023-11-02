import io

import pandas as pd
import xlsxwriter
from django.core.cache import cache

def create_workbook(request, data, title):
    """
    The function that controls the creation and formatting of
    polling tables.
    """
    cache_key = "tables_for_user_" + str(request.user.id)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ create main results polling table
        data.to_excel(writer, index=False, sheet_name='results')
        workbook = writer.book
        results_sheet = writer.sheets['results']

        results_sheet.set_zoom(90)
        header_format = workbook.add_format({
            "bg_color": "#951F06",
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
                results_sheet.write(i + 1, 3, question_value, question_format)

        # Loop through rows, starting from the fourth row, and apply the percentage format

        def format_percentages(data, sheet):
            """
            # Loop through rows, starting from the fourth row, 
            # and apply the percentage format
            """
            for row_num in range(3, len(data)):  # start from the fourth row (index 3)
                row_data = data.iloc[row_num]
                for col_num in range(5, len(data.columns)):  # start from the sixth column (index 5)
                    cell_value = data.iloc[row_num, col_num]
                    # Check if the cell contains a number (int or float)
                    if isinstance(cell_value, (int, float)):
                        # Apply percent format to the cell because it contains a number
                        sheet.write_number(row_num + 1, col_num, cell_value, percent_format)
                    elif pd.isna(cell_value) or cell_value == '':
                        # If the cell is NaN or an empty string, write an empty string
                        sheet.write_string(row_num + 1, col_num, '')
                    else:
                        # Otherwise, write the value as it is (this covers non-empty strings)
                        sheet.write(row_num + 1, col_num, cell_value)

        format_percentages(data, results_sheet)

        for col_num, value in enumerate(data.columns.values):
            results_sheet.write(0, col_num, value, header_format)

        # Loops through the question ids to create individual tables
        non_header_data = data.iloc[2:]
        header = data.loc[0:1]
        ids = non_header_data['IDs'].tolist()
        checked = []
        for qid in ids:
            if qid not in checked:
                sub_table = data[(data['IDs'] == qid)]
                concat_sub_table = pd.concat([header, sub_table], ignore_index=True)
                concat_sub_table.to_excel(
                    writer,
                    index=False,
                    sheet_name=f'question ID - {qid}'
                )
                question_sheet = writer.sheets[f'question ID - {qid}']
                format_percentages(concat_sub_table, question_sheet)
            checked.append(qid)
        writer.close()

    output.seek(0)
    cache.set(cache_key, output.getvalue(), timeout=300)
    return cache_key
