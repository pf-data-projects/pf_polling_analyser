"""
Defines the standard crossbreaks that will be used in the data analysis. 
"""

# GENDER ={"gender": ["Male", "Female", "Prefer not to say"]}
# AGE = {"age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]}
# REGION = {"region": [
#     "London", "South East", "South West", "East of England",
#     "West Midlands", "East Midlands", "Yorkshire and the Humber",
#     "North West", "North East", "Scotland", "Wales", "Northern Ireland"
# ]}

CROSSBREAKS = {
    "gender": ["Male", "Female"],
    "age": ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"],
    "region": [
        "London", "South East", "South West", "East of England",
        "West Midlands", "East Midlands", "Yorkshire and the Humber",
        "North West", "North East", "Scotland", "Wales", "Northern Ireland"
    ],
    "seg": ['AB', 'C1', 'C2', 'DE'],
    "children": ["yes, no"],
    "education": [
        "GCSE or equivalent (Scottish National/O Level)", 
        "A Level or equivalent (GCE/Higher/Advanced Higher)", 
        "University Undergraduate Degree (BA/BSc)", 
        "University Postgraduate Degree (MA/MSc/MPhil)",
        "Doctorate (PhD/DPHil)"
    ]
}
