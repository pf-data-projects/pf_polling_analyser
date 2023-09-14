import os
import time

import requests

if os.path.exists("env.py"):
    import env

def get_survey_responses(api_token, api_token_secret, survey_id):
    """
    A function that makes a get request to the Alchemer
    API and returns the responses to the survey specified.
    """
    # Base URL for the Alchemer API
    base_url = "https://api.alchemer.com"
    endpoint = f"/v5/survey/{survey_id}/surveyresponse"

    # Construct the full URL
    url = f"{base_url}{endpoint}"

    # Set the authentication parameters
    params = {
        "api_token": api_token,
        "api_token_secret": api_token_secret,
    }

    # Make the GET request with the authentication parameters
    response = requests.get(url, params=params, timeout=10)
    return response.json() if response.status_code == 200 else None

def get_responses_json(survey_id):
    """
    Makes a get request to the endpoint for the survey specified,
    processes the json response, dumping it into a separate file.
    """
    main_list = []
    response = get_survey_responses(
        api_token=os.environ["API_TOKEN"],
        api_token_secret=os.environ["API_SECRET"],
        survey_id=survey_id)
    pages = response['total_pages']
    for i in range(1, pages + 1):
        print(f'getting page {i} out of {pages} pages of data.')
        page_data = get_survey_responses(
            api_token=os.environ["API_TOKEN"],
            api_token_secret=os.environ["API_SECRET"],
            survey_id=survey_id
        )
        main_list.extend(page_data['data'])
        time.sleep(1)
    return main_list
