import pandas as pd


def run_weighting(survey_data, weight_proportions):
    """
    Runs IPF for datasets to add the weighting column.
    """
    # Load the weight proportions and survey data
    # weight_proportions = pd.read_excel("Weight_Proportions.xlsx")
    # survey_data = pd.read_excel("data2.xlsx", sheet_name="Worksheet")

    # Extract column names after the colon
    def extract_column_name(col_name):
        if ":" in col_name:
            return col_name.split(":")[1].strip()
        return col_name

    column_mapping = {col: extract_column_name(col) for col in survey_data.columns}
    survey_data_renamed = survey_data.rename(columns=column_mapping)

    # Map answers to social grade codes
    # Pls forgive the awfully long lines of strings here.
    # I can't find a way to multi-line without breaking it :(
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

    # Prepare the survey data
    survey_subset = survey_data_renamed[["How old are you?", "Which of the following best describes how you think of yourself?", "In what region of the UK do you live?", "seg"]]
    survey_subset.columns = ["Age", "Gender", "region", "seg"]
    bins = [18, 24, 34, 44, 54, 64, 74, 84, 150]
    labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", "85+"]
    survey_subset["Age Group"] = pd.cut(survey_subset["Age"], bins=bins, labels=labels, right=True, include_lowest=True)
    survey_subset["genderage"] = survey_subset["Gender"] + " " + survey_subset["Age Group"].astype(str)

    def ipf(survey_data, weight_proportions, max_iterations=100, convergence_threshold=0.001):
        survey_data['weight'] = 1.0
        for iteration in range(max_iterations):
            previous_weights = survey_data['weight'].copy()
            for _, row in weight_proportions.iterrows():
                group, specific, target_prop = row['Group'], row['Specific'], row['Proportion']
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

    # Apply IPF with region to the survey data
    ipf_result = ipf(survey_subset, weight_proportions)

    # Join the weight column from ipf_result to the original survey_data
    survey_data['weighted_respondents'] = ipf_result['weight']

    # # Save the dataset with appended weights to an output file
    # survey_data.to_excel("merged_weighted_data.xlsx")
    # ipf_result.to_csv("test_weight.csv", encoding="utf-8-sig")

    return survey_data
