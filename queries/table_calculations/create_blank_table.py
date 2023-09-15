"""
Creates a table filled with zeros.

The first column will be a list of questions/answers.
The subsequent columns will be a total column
and a column for each crossbreak.
"""

from .define_standard_crossbreaks import (GENDER, AGE, REGION)

TABLE = {
    'Answers': [],
    'Total': [],
    f'{GENDER[0]}': [],
    f'{GENDER[1]}': [],
    f'{AGE[0]}': [],
    f'{AGE[1]}': [],
    f'{AGE[2]}': [],
    f'{AGE[3]}': [],
    f'{AGE[4]}': [],
    f'{AGE[5]}': [],
    f'{REGION[0]}': [],
    f'{REGION[1]}': [],
    f'{REGION[2]}': [],
    f'{REGION[3]}': [],
    f'{REGION[4]}': [],
    f'{REGION[5]}': [],
    f'{REGION[6]}': [],
    f'{REGION[7]}': [],
    f'{REGION[8]}': [],
    f'{REGION[9]}': [],
    f'{REGION[10]}': [],
    f'{REGION[11]}': [],
}
