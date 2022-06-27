import random

import numpy as np
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.io import output_file, show
from bokeh.plotting import figure

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import GnBu5, OrRd5, OrRd9
from bokeh.models import ColumnDataSource, HoverTool

from preprocessing import transform_data

df = transform_data()
output_file("layout.html")

# Collect all unique activities
activities = df['Activity'].drop_duplicates().tolist()

"""
Concept flow of execution:
1. Group dataset by case variant
2. Within each group, collect by case id
3. Dynamically set the data ~ list of activities / waiting times
4. (Set a filter selector, allowing you to show whichever case variant one wants)
5. (Set tooltips, allowing you to hover whichever case variant one wants)
"""
c_list1 = ["#67001f", "#980043", "#ce1256", "#e7298a", "#df65b0", "#c994c7", "#d4b9da", "#e7e1ef", "#f7f4f9"]
c_list2 = ["#7f0000", "#b30000", "#d7301f", "#ef6548", "#fc8d59", "#fdbb84", "#fdd49e", "#fee8c8", "#fff7ec"]
c_list3 = ["#00441b", "#006d2c", "#238b45", "#41ae76", "#66c2a4", "#99d8c9", "#ccece6", "#e5f5f9", "#f7fcfd"]
# Color definitions for each activity:
grey = "#D3D3D3"  # Waiting time
reg_claim = "#FFE6CC"  # Light orange
quick_asse = "#FFF2CC"  # Light yellow
asse_claim = "#D5E8D4"  # Light green
fin_asse = "#E1D5E7"  # Light purple
ame_claim = "#F5F5F5"  # White smoke
ana_claim = "#F8CECC"  # Light red
ame_asse = "#B1DDF0"  # Light blue
appr_asse = "#BAC8D3"  # Pale aqua
comb_l = c_list1 + c_list2 + c_list3
test = []
for i in range(0, 36):
    test.append(random.choice(comb_l))
print(test)
test = test

df_v = df.groupby('case_variant')

tooltips = [('Case ID', '@activities')]

p_list = []
colors = []

for name, grouped in df_v:
    activities = grouped.groupby('case_id').head(100)['Activity'].tolist()
    print(activities)
    activities = []
    range = list(map(str, grouped['case_id'].drop_duplicates().tolist()))
    print(range)
    data = {'activities': range}

    test = grouped.groupby(['Activity'], sort=False)['relative_start_time']

    print(test)



    # TODO NOTES: How to resolve this issue?
    #  1. Iteration 1: Only group by activity -> Rework loops get reduced into
    #  one single activity and are not displayed properly.
    #  This method will work for the majority of flows though. Since we aim to keep rework as low as possible
    #  -
    #  2. Iteration 2: Instead of visualising the representation within one case variant, how can we
    #  represent a overview of a case variant comparable with other case variants without going into depth.
    #  -
    #  3. Iteration 3: Rework to collect all cases, including the ones with a rework loop. The arising issue here is
    #  finding a way for groupby to not merge rows together -> groupby with more than 1 column.
    #  Once this is handled the visualisations should be complete and accurate.


    # act = grouped.groupby(['Activity'], level=0, sort=False)
    # act2 = grouped.groupby('case_id', sort=False)
    # i = 0
    # TODO Right now the start time and case id group by make it so its not able to visualise groups that have more
    #  than 1 case id. Will have to rework a part of this.
    # for act_n, group in act2:
    #
    #     print(act_n)
    #     print(group)
    #
    # prev=0
    #
    # for act_n, group in act:
    #     if prev == 0:
    #         prev = act_n[2]
    #     print(group)
    #     print(act_n[2])
    #     if act_n[2] == prev:
    #         if i != 0:
    #             colors.append(grey)  # Color for waiting time.
    #             data["wt" + str(act) + str(i)] = group.waiting_time
            # print(i)
            # colors.append(random.choice(comb_l))  # Random color for activity
            # data[act_n[0] + str(i)] = group.processing_time
            # activities.append(act_n[0] + str(i))
            # print(act_n[0] + str(i))
            # i += 1
        # else:
        #     prev = act_n[2]
        #     i = 0
        #     break
        # print(str(act_n) + " " + str(i))
        # print(group.processing_time)
    print(colors)
    print(len(activities))
    print(len(colors))
    print(len(data))
    # print(data)

    p = figure(y_range=range, width=1800, height=900, x_range=(-100, 10000), title="Processing time by case_id")
    p.add_tools(HoverTool(tooltips=tooltips))
    p.hbar_stack(activities, y='activities', height=0.9, color=colors, source=ColumnDataSource(data),
                 legend_label=["%s" % x for x in activities])

    p_list.append(p)

    data = {'activities': range}



grid = gridplot(p_list, ncols=2, width=1800, height=600)

show(grid)
