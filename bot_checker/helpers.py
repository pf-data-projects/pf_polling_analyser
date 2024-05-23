"""
This file contains helper functions to keep views.py clean
"""
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Standard library
import re

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Internal
from queries.api_request.get_survey_questions import get_questions_json
from queries.api_request.get_processed_questions import (
    extract_questions_from_pages,
    extract_data_from_question_objects
)


def strip_html_tags(strings):
    """
    A function to clean data from API
    """
    # Pattern to remove all HTML tags
    html_tag_pattern = re.compile(r'<[^>]+>')

    cleaned_strings = []
    for string in strings:
        # Remove all HTML tags
        string = html_tag_pattern.sub('', string)
        # Replace newline characters with space
        string = string.replace('\n', ' ')
        cleaned_strings.append(string)
    return cleaned_strings


def get_questions(survey_id):
    """
    A func to call the Alchemer API and return a list of
    essay questions.
    """
    # Get data from API and clean it
    survey_questions = get_questions_json(survey_id)
    questions = extract_questions_from_pages(survey_questions)
    question_data = extract_data_from_question_objects(questions)
    # Filter for open responses
    question_data = question_data[question_data['question_type'] == "ESSAY"]
    essay_list = question_data['question_title'].to_list()
    essay_list = strip_html_tags(essay_list)
    return essay_list
