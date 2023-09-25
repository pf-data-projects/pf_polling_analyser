"""
Defines some common functions that will be used in data cleaning.
"""

def columns_with_substring(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question id.
    """
    return [
        col for col in df.columns if col.split(" : ", 1)[0] == substring
        ]


def columns_with_substring_question(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question title/text
    """
    return [
        col for col in df.columns if col.split(": ", 1)[1] == substring
        ]
