""" 
Defines the functions that will make requests to the
survey response API endpoints.
"""

import os
import time

import requests
import pandas as pd

from .get_processed_responses import process_responses
if os.path.exists("env.py"):
    import env

def get_survey_responses(api_token, api_token_secret, survey_id, page):
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
        "page": page
    }

    # Make the GET request with the authentication parameters
    session = requests.Session()
    response = session.get(url, params=params, timeout=10)
    return response.json() if response.status_code == 200 else None

def get_responses(survey_id):
    """
    TESTING - just gets data for one page
    so that I don't have to make requests for all pages
    and wait ages.
    """
    print("getting number of pages...")
    response = get_survey_responses(
        api_token=os.environ["API_TOKEN"],
        api_token_secret=os.environ["API_SECRET"],
        survey_id=survey_id,
        page=1
    )
    pages = response['total_pages']
    print(f'there are {pages} pages')
    data = {}
    data = pd.DataFrame(data)
    for i in range(1, pages + 1):
        print("page:", i)
        page_data = get_survey_responses(
            api_token=os.environ["API_TOKEN"],
            api_token_secret=os.environ["API_SECRET"],
            survey_id=survey_id,
            page=i
        )
        page_data = process_responses(page_data)
        if i > 1:
            # sticks all response data together into one df
            frames = [data, page_data]
            data = pd.concat(frames)
        else:
            data = page_data
    data.to_csv('DEFINITELY-A-TEST.csv', encoding="utf-8-sig", index=False)
    return data
