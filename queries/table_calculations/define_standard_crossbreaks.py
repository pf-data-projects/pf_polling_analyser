"""
Defines the standard crossbreaks that will be used in the data analysis. 
"""

# GENDER ={"gender": ["Male", "Female", "Prefer not to say"]}
# AGE = {"age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]}
# REGION = {"region": [
#     "London", "South East", "South West", "East of England",
#     "West Midlands", "East Midlands", "Yorkshire and the Humber",
#     "North West", "North East", "Scotland", "Wales", "Northern Ireland"
# ]}

CROSSBREAKS = {
    "gender": ["Male", "Female"],
    "age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    "region": [
        "London", "South East", "South West", "East of England",
        "West Midlands", "East Midlands", "Yorkshire and the Humber",
        "North West", "North East", "Scotland", "Wales", "Northern Ireland"
    ],
}

def columns_with_substring(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question id.
    """
    return [
        col for col in df.columns if col.split(": ", 1)[0] == substring
        ]


def columns_with_substring_question(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question title/text
    """
    return [
        col for col in df.columns
        if (": " in col) and (col.split(": ", 1)[1] == substring)
        ]

def columns_with_substring_answers(df, substring, qid):
    """
    Another helper function for checkbox questions
    """
    return [
        col for col in df.columns
        if qid in col and substring in col
    ]
