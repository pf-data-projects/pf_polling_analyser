import pandas as pd

def extract_questions_from_pages(question_data):
    """
    Loops through pages of the API response and
    creates a enw JSON file with all the survey questions.
    """
    pages = list(question_data['data']['pages'])

    # loops through all pages and adds the questions
    # on each page to a list of all survey questions.
    question_list = []
    for page in pages:
        questions = list(page['questions'])
        question_list.extend(questions)
    return question_list

def extract_data_from_question_objects(question_list):
    """
    Extracts the question ID, question text, and question type
    from the question objects in the question list.
    """
    question_ids = []
    question_texts = []
    question_types = []
    question_titles = []
    question_rebase = []

    for question in question_list:

        # checks if the question is shown to all respondents
        if question['properties']['required'] is True:
            question_rebase.append(False)
        elif question['properties']['required'] is False:
            question_rebase.append(True)

        print(question['id'], question['properties']['required'])

        # adds data from json dictionary to the lists
        question_ids.append(question['id'])
        question_texts.append(question['base_type'])
        question_types.append(question['type'])
        question_titles.append(question['title']['English'])

        # checks if the question has options and
        # adds their data to the lists
        if question['options']:
            for option in question['options']:
                question_ids.append(question['id'])
                question_texts.append('Option')
                question_types.append(question['type'])
                question_titles.append(option['title']['English'])
                question_rebase.append(not question['properties']['required'])

        # checks if the question has subquestions
        # and adds their data to the lists.
        if 'sub_questions' in question:
            for sub_question in question['sub_questions']:
                if sub_question['properties']['required'] is True:
                    question_rebase.append(False)
                elif sub_question['properties']['required'] is False:
                    question_rebase.append(True)
                print(sub_question['id'], sub_question['properties']['required'])
                question_ids.append(sub_question['id'])
                question_texts.append(sub_question['base_type'])
                question_types.append(sub_question['type'])
                question_titles.append(sub_question['title']['English'])

                # checks if the subquestion has options and
                # adds their data to the lists
                if sub_question['options']:
                    for option in sub_question['options']:
                        question_ids.append(sub_question['id'])
                        question_texts.append('Option')
                        question_types.append(sub_question['type'])
                        question_titles.append(option['title']['English'])
                        question_rebase.append(not sub_question['properties']['required'])

    # creates a dataframe from the lists and outputs to csv
    # with correct encoding for windows: "utf-8-sig"
    question_dict = {
        'question_id': question_ids,
        'question_text': question_texts,
        'question_type': question_types,
        'question_title': question_titles,
        'question_rebase': question_rebase
    }
    question_data = pd.DataFrame(question_dict)
    print(question_data.head())
    return question_data
