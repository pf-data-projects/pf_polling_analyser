"""
This file contains the logic to handle calling
various checks on each answer to each open response question

1. check_for_bots: loops over each essay question to apply
any of the specific checks to the dataset

2. call_openai: a function to load question and answer in a payload
to the OpenAI API to prompt with any number of checks

3. call_spacy_word_check: a function to generate a score for each 
answer based on how many words parse in English.
"""

import os

import pandas as pd
import numpy as np

import spacy
from openai import OpenAI

from queries.table_calculations.helpers import col_substr_partial

CLIENT = OpenAI(api_key=os.environ['OPENAI'])


def check_for_bots(self, essay_list, data, check):
    """
    A function to handle logic for calling openAI
    for each answer to each essay question.
    """
    print("number of open response questions", len(essay_list))
    print("rows in data:", len(data))
    k = 0
    self.update_state(
        state='PROGRESS',
        meta={'question': k, 'total': len(essay_list)}
    )
    for essay in essay_list:
        essay_col = col_substr_partial(data, essay)[0]
        filtered = data[essay_col]
        if check == 'sense':
            data[f'Sense score {essay}'] = filtered.apply(
                lambda x: call_openai(x, essay) if isinstance(x, str) else "No answer"
            )
            data = aggregate_score(data, "Sense score")
        if check == 'is_word':
            data[f'Word check score {essay}'] = filtered.apply(
                lambda x: call_spacy_word_check(x) if isinstance(x, str) else "No answer"
            )
            data = aggregate_score(data, "Word check score")
        if check == 'duplicate':
            data = find_duplicates(data, essay_col)
        self.update_state(
            state='PROGRESS',
            meta={'question': k + 1, 'total': len(essay_list)}
        )
    if check == 'duplicate':
        data = aggregate_score(data, "Duplicates")
    return data


def aggregate_score(data, string):
    """
    A function to take the checks performed on data
    and provide an average score for each respondent
    based on how many open responses they answered.
    """
    filtered = data.filter(like=string)
    filtered = filtered.replace("No answer", np.nan)
    filtered = filtered.apply(pd.to_numeric, errors='coerce')
    data['Average score'] = filtered.mean(axis=1)
    return data


def call_spacy_word_check(answer):
    """
    A function to handle checking if words
    in answers make sense.
    """
    nlp = spacy.load("en_core_web_lg")
    sentence = nlp(answer)
    word_count = sum(1 for token in sentence if token.is_alpha)
    valid_words = sum(1 for token in sentence if token.is_alpha and not token.is_oov)
    score = 0
    if word_count == 0 or valid_words == 0:
        return 0
    score = valid_words / word_count * 10
    score = round(score)
    print(score)
    return score


def find_duplicates(data, column_name):
    """
    A function to find duplicates in answers columns.
    """
    occurrence_dict = {}
    # First pass: Count occurrences of each string
    for value in data[column_name]:
        if value in occurrence_dict:
            occurrence_dict[value] += 1
        else:
            occurrence_dict[value] = 1
    # Second pass: Assign duplicate flag based on occurrences
    duplicate_flags = []
    for value in data[column_name]:
        if occurrence_dict[value] > 1:
            duplicate_flags.append(0)
        else:
            duplicate_flags.append(10)
    # Add the new column to the dataframe
    data[f'Duplicates {column_name}'] = duplicate_flags
    return data


def call_openai(answer, question):
    """ 
    A function to evaluate each answer for each
    question using AI.
    """
    prompt = f"""
    Providing your answer as just an integer and nothing more, 
    please give a score between 0 and 10 of how relevant the 
    following answer is to an example question 
    (where 0 is totally irrelevant and 10 is perfectly relevant):
    question: {question}
    answer: {answer}
    """
    messages = [{
        "role": "user",
        "content": prompt
    }]
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5
    )
    response_text = response.choices[0].message.content
    return response_text
