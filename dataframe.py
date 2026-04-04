import pandas as pd
import numpy as np
import json
import duckdb


# Load the data
with open('mines_catalog.json', 'r') as f:
    data = json.load(f)

# Convert directly
df = pd.DataFrame(data)


# Uses a lambda to remove the specific name from each corresponding row
df['name'] = df.apply(lambda x: x['name'].replace(x['code'] + '.', '').strip(), axis=1)
df['name'] = df.apply(lambda x: x['name'].replace(x['code'] + '.', '').strip(), axis=1)


query = """
SELECT
    code,
    split_part(name, '.', 1) AS title,
    regexp_extract(name, '(\d+[.-]\d+)') AS credithours,
    prereqs,
    coreqs

FROM df
"""

df_split = duckdb.query(query).to_df()

df_split = df_split.replace('None', np.nan, inplace=True)

coursedf = df_split
print(coursedf)

