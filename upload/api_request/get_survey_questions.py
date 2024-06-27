import os
import requests

def get_survey_questions(api_token, api_token_secret, id):
    """
    Makes a get request to the endpoint for the survey specified
    by the id passed and returns the survey's questions.
    """
    # Base URL for the Alchemer API
    base_url = "https://api.alchemer.com"
    endpoint = f"/v5/survey/{id}"

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

def get_questions_json(survey_id):
    """
    Makes a get request to the endpoint for the survey specified
    and returns survey question data to the view.
    """
    # print("getting data for this survey's questions...")
    survey_questions = get_survey_questions(
        api_token=os.environ.get("API_TOKEN"),
        api_token_secret=os.environ.get("API_SECRET"),
        id=survey_id
    )
    return survey_questions
