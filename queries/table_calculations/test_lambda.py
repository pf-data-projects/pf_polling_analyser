import pandas as pd

table = pd.read_csv("totals_calculated.csv")
results = pd.read_csv('DEFINITELY-A-TEST.csv')

total_respondents = len(results.index)
constant = total_respondents
print(constant)

table = table.applymap(lambda x: x / constant * 100 if isinstance(x, int) else x)

table.to_csv("test_percentage.csv", index=False, encoding="utf-8-sig")
