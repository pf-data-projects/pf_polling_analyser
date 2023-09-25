import pandas as pd

def clean_survey_legend(legend):
    """
    Takes the text extracted from word doc and gets:
    - QID
    - Type
    - Options

    for each question and returns the information
    as a pandas dataframe.
    """
    pages = legend.split(sep="\nPage")
    print(pages[0])
