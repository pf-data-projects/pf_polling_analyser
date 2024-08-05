"""
This file handles what will go into the cover page.
This will also be appended to the start of the polling
tables excel file as a separate sheet.
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
import pandas as pd

def create_cover_page(data, title, dates):
    """
    Create a dataframe containing all info needed
    for polling table cover page.
    """
    cover_list = []
    cover_list.append("")
    cover_list.append(f"Fieldwork carried out: {dates}")
    cover_list.append("Interview method: Online Survey")
    cover_list.append("Population represented: UK Adults")
    cover_list.append(f"Sample size: {round(data.at[1, 'Total'])}")
    cover_list.append("")
    cover_list.append("")
    cover_list.append("Methodology:")
    # sorry, I tried to make the strings below multiline
    # but ended up with some weird extra spaces in the excel output
    # ~J
    cover_list.append(
        "All results are weighted using Iterative Proportional Fitting, or 'Raking'. The results are weighted by interlocking age & gender, region and social grade to Nationally Representative Proportions"
    )
    cover_list.append("")
    cover_list.append("")
    cover_list.append(
        "Public First is a member of the BPC and abides by its rules. For more information please contact the Public First polling team:"
    )
    cover_list.append("polling@publicfirst.co.uk")
    cover = {
        f"Public First Poll For: {title}": cover_list,
    }
    cover_df = pd.DataFrame(cover)
    return cover_df
