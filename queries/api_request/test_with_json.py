import json
import pandas as pd

with open('response_list.json', 'r') as f:
    response_list = json.load(f)

valid = [x for x in response_list['data'] if x['status'] == 'Complete']

list_weird_question = []
for k in valid:
    if "208" not in k['survey_data']:
        print(k["id"])
