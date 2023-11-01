import pandas as pd
import xlsxwriter

def create_workbook(data, title):
    """
    The function that controls the creation and formatting of
    polling tables.
    """
    writer = pd.ExcelWriter(f'{title}.xlsx', engine='xlsxwriter')

    # create main results polling table
    data.to_excel(writer, index=False, sheet_name='results')
    workbook = writer.book
    results_sheet = writer.sheets['results']

    results_sheet.set_zoom(90)
    header_format = workbook.add_format({
        "bg_color": "#951F06",
        "bold": True,
        "font_color": "#FFFFFF"
    })
    for col_num, value in enumerate(data.columns.values):
        results_sheet.write(0, col_num, value, header_format)
    writer.close()
