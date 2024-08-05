"""
Defines the standard crossbreaks that will be used in the data analysis.
"""

from . import calc
from . import helpers
from .rebase import rebase

CROSSBREAKS = {
    "gender": ["Male", "Female"],
    "age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    "region": [
        "London", "South East", "South West", "East of England",
        "West Midlands", "East Midlands", "Yorkshire and the Humber",
        "North West", "North East", "Scotland", "Wales", "Northern Ireland"
    ],
    "region_gb": [
        "London", "South East", "South West", "East of England",
        "West Midlands", "East Midlands", "Yorkshire and the Humber",
        "North West", "North East", "Scotland", "Wales",
    ],
    "seg": ['AB', 'C1', 'C2', 'DE'],
    "children": ["Yes", "No"],
    "children(updated)": [
        "No children", "Yes - child/children aged under 5 years old",
        "Yes - child/children aged 5-10 years old", "Yes - child/children aged 11-15 years old",
        "Yes - child/children aged 16-18 years old", "Yes - child/children over 18 years old",
        "Prefer not to answer",
    ],
    "education": [
        "GCSE or equivalent (Scottish National/O Level)",
        "A Level or equivalent (GCE/Higher/Advanced Higher)",
        "Level 4 / 5 or equivalent (HND/HNC/Higher Apprenticeship)",
        "University Undergraduate Degree (BA/BSc)",
        "University Postgraduate Degree (MA/MSc/MPhil)",
        "Doctorate (PhD/DPHil)"
    ],
    "vote2019": [
        "The Brexit Party",
        "Conservative",
        "Labour",
        "Liberal Democrat",
        "I did not vote",
    ],
    "eu2016": [
        "Leave",
        "Remain",
        "I did not vote"
    ],
    "voting_intention": [
        "Conservative",
        "Labour",
        "Liberal Democrats",
    ],
    'area': [
        "Urban/City Centre",
        "Suburbs",
        "Large Town",
        "Small Town",
        "Village",
        "Rural Area",
    ],
    "income": [
        "No annual income",
        "Less than £10,000",
        "£10,000 - £14,999",
        "£15,000 - £19,999",
        "£20,000 - £24,999",
        "£25,000 - £29,999",
        "£30,000 - £34,999",
        "£35,000 - £39,999",
        "£40,000 - £44,999",
        "£45,000 - £49,999",
        "£50,000 - £59,999",
        "£60,000 - £69,999",
        "£70,000 - £79,999",
        "£80,000 - £89,999",
        "£90,000 - £99,999",
        "£100,000 or more",
    ],
    # business poll options
    "employee_number": [
        "2-4",
        "5-9",
        "10-24",
        "25-49",
        "50-99",
        "100-249",
        "250-499",
        "500-999",
        "1,000+",
    ],
    "company_age": [
        "Less than 1 year",
        "1-2 years",
        "2-5 years",
        "5-10 years",
        "10-20 years",
        "20-50 years",
        "More than 50 years",
    ],
    "annual_revenue": [
        "Under £85,000",
        "£85,001 to £250,000",
        "£250,001 to £500,000",
        "£500,001 to £1 million",
        "£1 million to £2 million",
        "£2 million to £5 million",
        "£5 million to £10 million",
        "£10 million to £20 million",
        "£20 million to £50 million",
        "Over £50 million",
    ]
}

QUESTIONS = {
    "gender": "Which of the following best describes how you think of yourself?",
    "age" : "How old are you?",
    "region": "In what region of the UK do you live?",
    "region_gb": "In what region of the UK do you live?",
    "seg": "Think about the Chief Income Earner in your household",
    "children": "Do you have any children under the age of 18 living at home?",
    "children(updated)": "Do you have any children? If so, how old are they?",
    "education": "What is the highest level of education you have achieved?",
    "vote2019": "Do you remember how you voted in the 2019 General Election, if you were able to vote?This was the most recent General Election in which Boris Johnson was the leader of the Conservative Party, and Jeremy Corbyn was the leader of the Labour Party",
    "eu2016": "How did you vote in the 2016 referendum on whether to Leave or Remain in the EU, if you were able to vote?",
    "voting_intention": "And, if a general election was called tomorrow, which party would you vote for?",
    "income": "What is the annual income of your household before tax?",
    "area": "Which of the following best describes the area where you live?",
    "employee_number": "How many employees does your company currently employ across all locations, including yourself?",
    "company_age": "How long has your business been operating for?",
    "annual_revenue": "What is the approximate annual revenue of your business?",
}


def calc_standard(value, col_index, cb_question, table, question_list, results, question_data):
    """
    A function that calls the general calc func
    for the crossbreak, col, and question supplied.
    """
    for question in question_list:
        get_cb = results[helpers.col_with_substr_q(results, cb_question)]
        filtered_df = results.loc[(results[get_cb.columns[0]] == value)]
        table.iat[0, col_index] = len(filtered_df.index)
        table.iat[1, col_index] = filtered_df['weighted_respondents'].astype(float).sum()
        table = calc.calc(filtered_df, col_index, table, question, results, question_data, False)
    return table

def rebase_standard(value, col_index, cb_question, table, question_list, results, question_data):
    """
    A function that calls the rebase func
    for the crossbreak, col, and question supplied.
    """
    get_gender = results[helpers.col_with_substr_q(results, cb_question)]
    filtered_df = results.loc[(results[get_gender.columns[0]] == value)]
    table = rebase(question_data, filtered_df, question_list, table, col_index)
    return table
