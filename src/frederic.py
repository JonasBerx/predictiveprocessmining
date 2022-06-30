"""
    WEDNESDAY FEEDBACK DISCUSSION:

    - REPRESENT DISTRIBUTION OF WAITING TIMES AND ACTIVITY TIMES SEPARATELY.
    - REPRESENT THROUGH A STACKED BAR PLOT WITHOUT OUTLIERS.
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
import colorcet as cc
from numpy import linspace
from scipy.stats.kde import gaussian_kde

from bokeh.models import ColumnDataSource, FixedTicker, PrintfTickFormatter
from bokeh.plotting import figure, show
from bokeh.sampledata.perceptions import probly

from preprocessing import transform_data

df = transform_data()
output_file("fre.html")


def ridge(category, data, scale=20):
    return list(zip([category] * len(data), scale * data))


p_list = []

valid_df = df.groupby('case_variant').filter(lambda x: x['case_id'].nunique() > 3)

df_c = valid_df.groupby('case_variant')

for name, value in df_c:
    categories = value['Activity'].drop_duplicates().tolist()  # All the possible activities
    case_df = value.groupby('case_id')

    data = {}
    cases = list(map(int, value['case_id'].drop_duplicates().tolist()))

    for case in cases:
        # print(case)
        # print(data)
        i = 0
        df = case_df.get_group(int(case))
        df = df.groupby(['Activity', 'start_time', 'processing_time', 'waiting_time'], sort=False)
        # print(df.head(5))
        for k, v in df:
            # print(k)
            # print(v)
            i += 1

            if (k[0]).strip() + str(i) in data:
                data[(k[0]).strip() + str(i) + 'wt'] += [k[3]]
                data[(k[0]).strip() + str(i)] += [k[2]]
            else:
                data[(k[0]).strip() + str(i) + 'wt'] = [k[3]]
                data[(k[0]).strip() + str(i)] = [k[2]]

    categories = list(data.keys())
    print("----")
    # print(name)
    # print(cases)
    # print(value)
    # print(data)
    # print(categories)
    p = figure(y_range=categories)
    for act, l in data.items():
        print(categories)
        print(l)

        p.hbar(y=cases, right=l)

    show(p)
    break