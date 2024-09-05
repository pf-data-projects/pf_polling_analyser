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
    question_sort = []

    # makes previous question data available to
    # question in a loop.
    prev_question = {}

    for question in question_list:

        # checks if the question is shown to all respondents
        if 'required' in question['properties']:
            if question['properties']['required'] is True:
                question_rebase.append(False)
            elif question['properties']['required'] is False:
                question_rebase.append(False)
        else:
            question_rebase.append('N/A')

        # checks if the question has randomised answer order
        if 'option_sort' in question['properties']:
            randomised = question['properties']['option_sort'] == 'SHUFFLE'
            if randomised and question["type"] == 'RADIO':
                question_sort.append(True)
            else:
                question_sort.append(False)
        else:
            question_sort.append(False)

        # adds data from json dictionary to the lists
        question_ids.append(question['id'])
        question_texts.append(question['base_type'])
        question_types.append(question['type'])
        question_titles.append(question['title']['English'])

        # handle non-grid piped answers
        if 'pipe_values_from' in question:
            parent_id = int(question['pipe_values_from'])
            for q in question_list:
                if q['id'] == parent_id:
                    parent = q
            for option in parent['options']:
                if option['title']['English'] in ["Don't Know", "Don’t know", "Don't know"]:
                    continue
                if 'None of the above' in option['title']['English']:
                    continue
                question_ids.append(question['id'])
                question_texts.append('Option')
                question_types.append(question['type'])
                question_titles.append(option['title']['English'])
                question_rebase.append(False)
                question_sort.append(False)

        # checks if the question has options and
        # adds their data to the lists
        if question['options']:
            for option in question['options']:
                if question['type'] == "RANK":
                    question_ids.append(question['id'])
                    question_texts.append('Option')
                    question_types.append(question['type'])
                    question_titles.append(option['title']['English'])
                    question_rebase.append(False)
                    question_sort.append(False)
                    for i in range(len(question['options'])):
                        question_ids.append(question['id'])
                        question_texts.append('sub_option')
                        question_types.append(question['type'])
                        question_titles.append(i + 1)
                        question_rebase.append(False)
                        question_sort.append(False)

                else:
                    question_ids.append(question['id'])
                    question_texts.append('Option')
                    question_types.append(question['type'])
                    question_titles.append(option['title']['English'])
                    question_rebase.append(False)
                    if 'option_sort' in question['properties']:
                        randomised = question['properties']['option_sort'] == 'SHUFFLE'
                        if randomised and question["type"] == 'RADIO':
                            question_sort.append(True)
                        else:
                            question_sort.append(False)
                    else:
                        question_sort.append(False)

        # checks if the question has subquestions
        # and adds their data to the lists.
        if 'sub_questions' in question:
            for sub_question in question['sub_questions']:
                if 'attention' in sub_question['title']['English']:
                    continue
                if sub_question['properties']['required'] is True:
                    question_rebase.append(False)
                elif sub_question['properties']['required'] is False:
                    question_rebase.append(False)
                question_ids.append(question['id'])
                question_texts.append(f"sub_{sub_question['base_type']}")
                question_types.append(f"{question['type']} | {sub_question['type']}")
                question_titles.append(sub_question['title']['English'])
                question_sort.append(False)

                # checks if the subquestion has options and
                # adds their data to the lists
                if sub_question['options']:
                    for option in sub_question['options']:
                        question_ids.append(question['id'])
                        question_texts.append('sub_option')
                        question_types.append(f"{question['type']} | {sub_question['type']}")
                        question_titles.append(option['title']['English'])
                        question_rebase.append(False)
                        question_sort.append(False)


        # Code to handle edge case where a table question relies on options
        # of a question immediately before it.
        # if question['type'] == 'TABLE' and 'sub_questions' not in question:
        #     for sub_question in prev_question['options']:
        #         if 'Don’t know' in sub_question['title']['English'] or 'None of the above' in sub_question['title']['English']:
        #             continue
        #         question_ids.append(question['id'])
        #         question_texts.append('sub_Question')
        #         question_titles.append(sub_question['title']['English'])
        #         question_types.append(f"{question['type']} | RADIO")
        #         question_rebase.append(False)
        #         for option in question['options']:
        #             question_ids.append(question['id'])
        #             question_texts.append('sub_option')
        #             question_types.append(f"{question['type']} | RADIO")
        #             question_titles.append(option['title']['English'])
        #             question_rebase.append(False)

        # prev_question = question

        # Rewrite the code above to get options by searching
        # based on the piped_from attribute in the api response.

        if question['type'] == 'TABLE' and 'piped_from' in question['properties']:
            parent_id = int(question['properties']['piped_from'])
            for q in question_list:
                if q['id'] == parent_id:
                    parent = q
                    # print(parent)
            for sub_question in parent['options']:
                # don't pipe through 'don't know' and
                # 'none of the above' to grid because
                # it won't make sense.
                if 'Don’t know' in sub_question['title']['English'] or 'None of the above' in sub_question['title']['English']:
                    continue
                if "Don't Know" in sub_question['title']['English']:
                    continue
                if "Don't know" in sub_question['title']['English']:
                    continue
                question_ids.append(question['id'])
                question_texts.append('sub_Question')
                question_titles.append(sub_question['title']['English'])
                question_types.append(f"{question['type']} | RADIO")
                question_rebase.append(False)
                question_sort.append(False)

                for option in question['options']:
                    question_ids.append(question['id'])
                    question_texts.append('sub_option')
                    question_types.append(f"{question['type']} | RADIO")
                    question_titles.append(option['title']['English'])
                    question_rebase.append(False)
                    question_sort.append(False)

    # creates a dataframe from the lists and outputs to csv

    question_dict = {
        'question_id': question_ids,
        'question_text': question_texts,
        'question_type': question_types,
        'question_title': question_titles,
        'question_rebase': question_rebase,
        'question_sort': question_sort
    }
    question_data = pd.DataFrame(question_dict)

    question_data['question_title'] = question_data['question_title'].str.strip()

    question_data.to_csv('question_data.csv', encoding='utf-8-sig')
    return question_data
