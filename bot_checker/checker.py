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

import pandas as pd

import spacy

from queries.table_calculations.helpers import col_substr_partial


def check_for_bots(essay_list, data, check):
    """
    A function to handle logic for calling openAI
    for each answer to each essay question.
    """
    print("number of open response questions", len(essay_list))
    print("rows in data:", len(data))
    for essay in essay_list:
        essay_col = col_substr_partial(data, essay)[0]
        filtered = data[essay_col]
        if check == 'test':
            return data
        # data[f'Sense score {essay}'] = filtered.apply(
        #     lambda x: call_openai(x, essay) if isinstance(x, str) else "No answer"
        # )
        if check == 'is_word':
            data[f'Word check score {essay}'] = filtered.apply(
                lambda x: call_spacy_word_check(x) if isinstance(x, str) else "No answer"
            )
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


def call_openai(answer, question):
    """ 
    A function to evaluate each answer for each
    question using AI.
    """
    print("Eyup world")
    return "Eyup world"
