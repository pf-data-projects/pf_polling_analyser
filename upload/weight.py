"""
This file handles the weighting of survey respondents via
a method called iterative proportional fitting.

The run_weighting function handles the overall logic
as well as preparing the columns of data that will be 
used in the weighting process

There is a helper function that extracts columns with
substrings. This makes it easier to work with pandas here.

ipf is a function that handles applying each respondent a weight
and then adjusting it gradually according to the different
categories. The function returns the same user-submitted 
survey results but this time with an extra column on the end
specifying each respondent's weight.

~~ Currently the questions used to define the IPF are
hardcoded. It also won't work unless there is a specific set of
weight proportions uploaded. In future this could be updated to
take user inputs for which questions to use, as well as being
able to take custom weight files as inputs. ~~

The apply_no_weight function simply adds a column to the end of
the file applying a weight of '1' to each person (i.e., no weight
at all because everyone has the same weight).
"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party
import pandas as pd

def run_weighting(survey_data, weight_proportions, 
    questions=None, groups=None, standard_weights=None):
    """
    Runs IPF for datasets to add the weighting column.
    """

    # Extract column names after the colon
    def extract_column_name(col_name):
        if ":" in col_name:
            return col_name.split(":")[1].strip()
        return col_name

    column_mapping = {col: extract_column_name(col) for col in survey_data.columns}
    survey_data_renamed = survey_data.rename(columns=column_mapping)

    # ~~~~~~~~~~~ Map answers to social grade codes
    # ~~~~~~~~~~~ Pls forgive the awfully long lines of strings here.
    # ~~~~~~~~~~~ I can't find a way to multi-line without breaking it :(
    SEG_Lookup = pd.DataFrame({
        "Answers": [
            "Casual worker - not in permanent employment",
            "Full-time carer of other household member",
            "Higher managerial/ professional/ administrative (e.g. Established doctor, Solicitor, Board Director in a large organisation (200+ employees, top level civil servant/public service employee))",
            "Housewife/Househusband/Homemaker",
            "Intermediate managerial/ professional/ administrative (e.g. Newly qualified (under 3 years) doctor, Solicitor, Board director small organisation, middle manager in large organisation, principle officer in civil service/local government)",
            "Other (Please Specify)",
            "Retired and living on state pension",
            "Semi or unskilled manual work (e.g. Manual workers, all apprentices to be skilled trades, Caretaker, Park keeper, non-HGV driver, shop assistant)",
            "Skilled manual worker (e.g. Skilled Bricklayer, Carpenter, Plumber, Painter, Bus/ Ambulance Driver, HGV driver, AA patrolman, pub/bar worker, etc.)",
            "Student",
            "Supervisory or clerical/junior managerial/professional/administrative (e.g. Office worker, Student Doctor, Foreman with 25+ employees, salesperson, etc.)",
            "Unemployed or not working due to long-term sickness"
        ],
        "Codes": [
            "E", "E", "A", "E", 
            "B", "0", "E", "D", 
            "C2", "C1", "C1", "E"
        ]
    })

    seg_col_name = next(
        col for col in survey_data_renamed.columns if 
        "Think about the Chief Income Earner in your household" in col
    )
    survey_data_renamed['seg'] = survey_data_renamed[seg_col_name].map(
        SEG_Lookup.set_index('Answers')['Codes']
    )

    region_column = None
    for col in survey_data_renamed.columns:
        if 'In what region of the UK do you live?' in col:
            region_column = 'region'
            break

    if region_column is None:
        raise KeyError('Region column not found in survey data.')

    # Prepare the survey data
    survey_subset = survey_data_renamed[
        [
            "How old are you?", 
            "Which of the following best describes how you think of yourself?", 
            "In what region of the UK do you live?", 
            "seg"
        ]
    ]
    survey_subset.columns = ["Age", "Gender", "region", "seg"]
    bins = [18, 24, 34, 44, 54, 64, 74, 84, 150]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", "85+"]
    survey_subset["Age Group"] = pd.cut(
        survey_subset["Age"], bins=bins, labels=labels, 
        right=True, include_lowest=True
    )
    survey_subset["genderage"] = survey_subset["Gender"] + " " + survey_subset["Age Group"].astype(str)

    def ipf(survey_data, weight_proportions, max_iterations=3, convergence_threshold=0.001):
        """
        Iterates up to the max iterations val unless 
        convergence threshold reached.

        Within this, the code iterates through each category
        specified in weight proportions and applies weights
        to each relevant respondent based on the UK proportions.
        """
        survey_data['weight'] = 1.0
        survey_data['is_non_binary'] = survey_data['Gender'].apply(lambda x: x not in ['Male', 'Female'])
        for iteration in range(max_iterations):
            previous_weights = survey_data['weight'].copy()
            for _, row in weight_proportions.iterrows():
                group, specific, target_prop = row['Group'], row['Specific'], row['Proportion']
                # Handling region weighting
                if group == 'region':
                    region_column = 'region'
                    subset = survey_data[survey_data[region_column] == specific]
                    current_prop = subset['weight'].sum() / survey_data['weight'].sum()
                    scaling_factor = target_prop / current_prop
                    survey_data.loc[survey_data[region_column] == specific, 'weight'] *= scaling_factor
                if group == "Overall":
                    total_weight = survey_data['weight'].sum()
                    scaling_factor = target_prop * len(survey_data) / total_weight
                    survey_data['weight'] *= scaling_factor
                else:
                    subset = survey_data[survey_data[group] == specific]
                    if group == "genderage":
                        if not subset.empty:
                            subset = subset[~subset['is_non_binary'] == True]
                    current_prop = subset['weight'].sum() / survey_data['weight'].sum()
                    scaling_factor = target_prop / current_prop
                    survey_data.loc[survey_data[group] == specific, 'weight'] *= scaling_factor
            weight_change = (survey_data['weight'] - previous_weights).abs().sum()
            if weight_change < convergence_threshold:
                break
        return survey_data
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Apply IPF with region to survey data
    ipf_result = ipf(survey_subset, weight_proportions)
    # ~~~~~~~~~~ Join weight column from ipf_result to the original survey_data
    survey_data['weighted_respondents'] = ipf_result['weight']
    return survey_data


def apply_no_weight(survey_data):
    """
    Adds an extra column to the survey data,
    assigning each respondent with the value 1
    rather than a weight.
    """
    survey_data['weighted_respondents'] = 1
    return survey_data

def apply_custom_weight(survey_data, weight_proportions, questions, groups, standard_weights):
    """
    A function for applying custom weights to 
    data.
    """
    def extract_column_name(col_name):
        if ":" in col_name:
            return col_name.split(":")[1].strip()
        return col_name

    column_mapping = {col: extract_column_name(col) for col in survey_data.columns}
    survey_data_renamed = survey_data.rename(columns=column_mapping)

    survey_subset = survey_data_renamed[questions]
    survey_subset.columns = [group for group in groups]
    standard_weights_cols = []

    if 'seg' in standard_weights:
        SEG_Lookup = pd.DataFrame({
            "Answers": [
                "Casual worker - not in permanent employment",
                "Full-time carer of other household member",
                "Higher managerial/ professional/ administrative (e.g. Established doctor, Solicitor, Board Director in a large organisation (200+ employees, top level civil servant/public service employee))",
                "Housewife/Househusband/Homemaker",
                "Intermediate managerial/ professional/ administrative (e.g. Newly qualified (under 3 years) doctor, Solicitor, Board director small organisation, middle manager in large organisation, principle officer in civil service/local government)",
                "Other (Please Specify)",
                "Retired and living on state pension",
                "Semi or unskilled manual work (e.g. Manual workers, all apprentices to be skilled trades, Caretaker, Park keeper, non-HGV driver, shop assistant)",
                "Skilled manual worker (e.g. Skilled Bricklayer, Carpenter, Plumber, Painter, Bus/ Ambulance Driver, HGV driver, AA patrolman, pub/bar worker, etc.)",
                "Student",
                "Supervisory or clerical/junior managerial/professional/administrative (e.g. Office worker, Student Doctor, Foreman with 25+ employees, salesperson, etc.)",
                "Unemployed or not working due to long-term sickness"
            ],
            "Codes": ["E", "E", "A", "E", "B", "0", "E", "D", "C2", "C1", "C1", "E"]
        })
        seg_col_name = next(col for col in survey_data_renamed.columns if "Think about the Chief Income Earner in your household" in col)
        survey_data_renamed['seg'] = survey_data_renamed[seg_col_name].map(SEG_Lookup.set_index('Answers')['Codes'])
        standard_weights_cols.append('seg')

    if 'genderage' in standard_weights:
        # standard_weights_cols.append("How old are you?")
        # standard_weights_cols.append("Which of the following best describes how you think of yourself?")
        bins = [18, 24, 34, 44, 54, 64, 74, 84, 150]
        labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", "85+"]
        survey_data_renamed["Age Group"] = pd.cut(survey_data_renamed["How old are you?"], bins=bins, labels=labels, right=True, include_lowest=True)
        survey_data_renamed["genderage"] = survey_data_renamed["Which of the following best describes how you think of yourself?"] + " " + survey_data_renamed["Age Group"].astype(str)
        standard_weights_cols.append('genderage')

    if 'region' in standard_weights:
        survey_data_renamed['region'] = survey_data_renamed['In what region of the UK do you live?']
        standard_weights_cols.append('region')

    if len(standard_weights) > 0:
        survey_subset_standard = survey_data_renamed[standard_weights_cols]
        survey_subset = pd.concat([survey_subset, survey_subset_standard], axis=1)
        survey_subset.to_csv('custom_and_standard_weights.csv')


    def custom_ipf(
        survey_data, weight_proportions,
        max_iterations=100, convergence_threshold=0.001
    ):
        """
        Function that handles iteration.
        """
        survey_data['weight'] = 1.0
        for iteration in range(max_iterations):
            previous_weights = survey_data['weight'].copy()
            for _, row in weight_proportions.iterrows():
                group, specific, target_prop = row['Group'], row['Specific'], row['Proportion']
                if target_prop == 0:
                    continue
                if group == "Overall":
                    total_weight = survey_data['weight'].sum()
                    scaling_factor = target_prop * len(survey_data) / total_weight
                    survey_data['weight'] *= scaling_factor
                else:
                    subset = survey_data[survey_data[group] == specific]
                    current_prop = subset['weight'].sum() / survey_data['weight'].sum()
                    scaling_factor = target_prop / current_prop
                    survey_data.loc[survey_data[group] == specific, 'weight'] *= scaling_factor
            weight_change = (survey_data['weight'] - previous_weights).abs().sum()
            if weight_change < convergence_threshold:
                break
        return survey_data

    ipf_result = custom_ipf(survey_subset, weight_proportions)
    survey_data['weighted_respondents'] = ipf_result['weight']
    return survey_data
