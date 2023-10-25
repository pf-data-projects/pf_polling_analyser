"""
Extra functions that help 
"""

def col_with_substr(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question id.
    """
    return [
        col for col in df.columns if col.split(": ", 1)[0] == substring
    ]

def col_with_substr_q(df, substring):
    """
    Helper function that returns the column
    of a dataframe which contains a specified substring.

    Searches by question title/text
    """
    return [
        col for col in df.columns
        if (": " in col) and (col.split(": ", 1)[1] == substring)
    ]

def col_with_substr_a(df, substring, qid):
    """
    Another helper function for checkbox questions.
    Checks column that contain both
    question ID and answer (substring)
    """
    return [
        col for col in df.columns
        if qid in col and substring in col
    ]

def col_with_qid(df, qid):
    """
    Returns a dataframe with all the columns
    that contain a question ID
    """
    return [
        col for col in df.columns if f"{qid}:" in col
    ]
