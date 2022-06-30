"""
This is a first try at trying to combine the data from one case variant to create a plot that represents the rough outline of a case variant's distribution
This idea is as following:
1. Gather all data from a case variant
2. Retain only Q1 through Q3 distro
3. Build a stacked bar chart from the cut data.

--

How will the data look like?
- List of the different case variants.
- List of the processing times of each activity -> List of activity 1, List of activity 2, ...
- Color scheme for each activity type.

"""

import numpy as np
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.io import output_file, show
from bokeh.plotting import figure

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import GnBu5, OrRd5, OrRd9
from bokeh.models import ColumnDataSource, HoverTool
from itertools import islice
from scipy.stats import norm

from preprocessing import transform_data

df = transform_data()
output_file("merger.html")


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)



# STEP 1: List of CASE VARIANTS

case_v_dict = {}
df_v = df.groupby('case_variant')

test_df = df_v.get_group( 790337521760341813)

#TODO Uncomment this later
# for name, grouped in df_v:
#     range = list(map(str, grouped['case_id'].drop_duplicates().tolist()))
#     case_v_dict[name] = {'occ': len(range), 'cases': range}

# print(case_v_dict)
# print(test_df)

# TODO THIS IS ONLY VIABLE FOR CASE VARIANTS WITH NO REWORK LOOPS
test_df['idx'] = test_df.groupby(['Activity'], sort=False).ngroup()

print(test_df.head(20))

# STEP 2: Calculate Q1 - Q3 for each activity within a case variant.
range = list(map(str, test_df['case_id'].drop_duplicates().tolist()))

# 'cases': range
data = {}
tdf = test_df.groupby(['idx', 'Activity'])

f = tdf.relative_start_time.quantile([0.25,0.5,0.75])

print(f)


ftivities = test_df.groupby('case_id')['Activity'].head(100).tolist()

rework_to_register = ftivities.count(' Register Claim')
# print(int(rework_to_register/len(range))+1)
if rework_to_register > len(range):
    idx = nth_index(ftivities, ' Register Claim', int(rework_to_register/len(range))+1)
else:
    idx = nth_index(ftivities, ' Register Claim', 2)
    # print(idx)

# print(ftivities)
if idx != None:
    ftivities = ftivities[:idx]
else:
    ftivities = ftivities

# print(ftivities)
activities = []
i = 0
for a in ftivities:
    i += 1
    activities.append(a + str(i) + 'wt')
    activities.append(a + str(i))


case_df = test_df.groupby('case_id')

for case in range:
    i = 0
    df = case_df.get_group(int(case))
    df = df.groupby(['Activity', 'start_time', 'processing_time', 'waiting_time'], sort=False)

    for k, v in df:
        i += 1

        if k[0] + str(i) in data:
            data[k[0] + str(i) + 'wt'] += [k[3]]
            data[k[0] + str(i)] += [k[2]]
        else:
            data[k[0] + str(i) + 'wt'] = [k[3]]
            data[k[0] + str(i)] = [k[2]]

# print(data)
res = {}

for k, v in data.items():
    # print(v)
    mu, std = norm.fit(v)
    # print(mu)
    # print(std)