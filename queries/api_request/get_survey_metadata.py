import json
import os
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 3rd party libraries
import requests


if os.path.exists('env.py'):
    import env

def get_survey_list(endpoint, api_token, api_token_secret, page):
    """
    Make a GET request to the Alchemer API.
    Args:
    - endpoint (str): The specific Alchemer endpoint.
    - api_token (str): Your API token.
    - api_token_secret (str): Your API token secret.
    
    Returns:
    - dict: The JSON response from the API.
    """

    # Base URL for the Alchemer API
    base_url = "https://api.alchemer.com"

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

    # Check for a successful response
    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code)
        response.raise_for_status()


def get_all_pages_of_surveys():
    """
    Makes a series of GET requests to the Alchemer API
    to get all the pages of survey data.
    """
    main_list = []
    response = get_survey_list(
        endpoint="/v5/survey",
        api_token=os.environ["API_TOKEN"],
        api_token_secret=os.environ["API_SECRET"],
        page=1)
    pages = response['total_pages']
    for i in range(1, pages + 1):
        print(f'getting page {i} out of {pages} pages of data.')
        page_data = get_survey_list(
            endpoint="/v5/survey",
            api_token=os.environ["API_TOKEN"],
            api_token_secret=os.environ["API_SECRET"],
            page=i)
        main_list.extend(page_data['data'])

    return main_list
