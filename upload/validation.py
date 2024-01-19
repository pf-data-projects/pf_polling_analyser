""" 
This file contains validation functions that check user inputs will work 

1. validate_cb_inputs takes standard cbs and data to check and ensure
users can't submit crossbreaks which don't exist in the data.
"""

def validate_cb_inputs(data, standard_cb):
    """
    Checks whether the standard cbs the user has selected
    exist in the dataset.
    """
    crossbreaks = [
        ['gender', "Which of the following best describes how you think of yourself?"],
        ['age', "How old are you?"],
        ['region', "In what region of the UK do you live?"],
        ['seg', "Think about the Chief Income Earner in your household"],
        ['children', "Do you have any children under the age of 18 living at home?"],
        [
            'education', 
            [
                "What is the highest level of education you have achieved?", 
                "What is the highest level of education you have achieved?"
            ]
        ],
    ]

    for cb in crossbreaks:
        if cb[0] in standard_cb:
            present = False
            for col in data.columns:
                if cb[0] == 'education':
                    if cb[1][0] in col or cb[1][1] in col:
                        present = True
                elif cb[1] in col:
                    present = True
            if not present:
                return [False, f'There is no {cb[0]} question in this data']
    return [True, "Standard CB validated"]
