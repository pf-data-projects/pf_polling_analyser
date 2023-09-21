""" 
Defines the functions that will make requests to the
survey response API endpoints.
"""

import os
import time

import requests
import pandas as pd

# from . import get_processed_responses
from get_processed_responses import process_responses
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
    response = requests.get(url, params=params, timeout=10)
    return response.json() if response.status_code == 200 else None

# def get_responses_json(survey_id):
#     """
#     Makes a get request to the endpoint for the survey specified,
#     processes the json response, dumping it into a separate file.
#     """
#     main_list = []
#     response = get_survey_responses(
#         api_token=os.environ["API_TOKEN"],
#         api_token_secret=os.environ["API_SECRET"],
#         survey_id=survey_id,
#         page=1)
#     pages = response['total_pages']
#     for i in range(1, pages + 1):
#         print(f'getting page {i} out of {pages} pages of data.')
#         page_data = get_survey_responses(
#             api_token=os.environ["API_TOKEN"],
#             api_token_secret=os.environ["API_SECRET"],
#             survey_id=survey_id,
#             page=i
#         )
#         main_list.extend(page_data['data'])
#         time.sleep(1)
#     return main_list

def get_responses_json(survey_id):
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
            frames = [data, page_data] # This line and the next should add pages of results together.
            data = pd.concat(frames)
        else:
            data = page_data
    print(data)
    data.to_csv('DEFINITELY-A-TEST.csv', encoding="utf-8-sig", index=False)

# print("hello!")
get_responses_json(7499039)

def testy_test(survey_id):
    response = get_survey_responses(
        api_token=os.environ["API_TOKEN"],
        api_token_secret=os.environ["API_SECRET"],
        survey_id=survey_id,
        page=12
    )
    data = process_responses(response)
    # print(data)

# testy_test(7499039)
