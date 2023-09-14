def get_survey_id(survey_list, survey_name):
    """
    Prompts the user to enter the title of the survey
    they want to access and returns the survey id.
    """
    survey_id = ""
    for survey in survey_list:
        if survey['title'] == survey_name:
            survey_id = survey['id']
        else:
            continue
    if survey_id == "":
        print("Survey not found.")
        return None
    return survey_id
