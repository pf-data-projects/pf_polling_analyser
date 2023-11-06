import pandas as pd

def create_cover_page(data):
    """
    Create a dataframe containing all info needed
    for polling table cover page.
    """
    cover_list = []
    cover_list.append("")
    cover_list.append("Interview method: Online Survey")
    cover_list.append("Population represented: UK Adults")
    cover_list.append(f"Sample size: {data.at[1, 'Total']}")
    cover_list.append("")
    cover_list.append("Methodology:")
    cover_list.append("All results are weighted using Iterative Proportional Fitting, or 'Raking'. The results are  weighted by interlocking age & gender, region and social grade to Nationally Representative Proportions")
    cover_list.append("")
    cover_list.append("Public First is a member of the BPC and abides by its rules. For more information please contact the Public First polling team:")
    cover_list.append("polling@publicfirst.co.uk")

    cover = {"Public First Poll for: ": cover_list}
    cover_df = pd.DataFrame(cover)

    print(cover_df)
    return cover_df
