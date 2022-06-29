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
from itertools import islice

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
waiting = "#D3D3D3"  # Grey
# reg_claim = "#FFE6CC"  # Light orange
# quick_asse = "#FFF2CC"  # Light yellow
# asse_claim = "#D5E8D4"  # Light green
# fin_asse = "#E1D5E7"  # Light purple
# ame_claim = "#F5F5F5"  # White smoke
# ana_claim = "#F8CECC"  # Light red
# ame_asse = "#B1DDF0"  # Light blue
# appr_asse = "#BAC8D3"  # Pale aqua

# This dict is currently for showcase. There needs to be a way to dynamically
# generate colors for unique activities which will then be used for the further processing.
color_dict = {
    ' Register Claim': '#FFE6CC',
    ' Quick Assessment': '#FFF2CC',
    ' Finalize Assessment': '#E1D5E7',
    ' Approve Assessment': '#BAC8D3',
    ' Amend Assessment': '#B1DDF0',
    ' Assess Claim': '#F8CECC',
    ' Analyze Claim': '#f7fcfd',
    ' Amend Claim': '#00441b',
    ' Prepare Claim Settlement': '#df65b0',
    ' Approve Claim Settlement': '#BAC8D3',
    ' Amend Claim Settlement': '#F5F5F5',
    ' Execute Claim Settlement': '#41ae76',
    ' Request Customer Info': '#fdd49e'

}

# comb_l = c_list1 + c_list2 + c_list3
# test = []
# for i in range(0, 36):
#     test.append(random.choice(comb_l))
# print(test)
# test = test

df_v = df.groupby('case_variant')

tooltips = [('Case ID', '@cases')]

p_list = []
p_dict = {}
colors = []


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

vv = 0
for name, grouped in df_v:
    range = list(map(str, grouped['case_id'].drop_duplicates().tolist()))
    # print(range)
    data = {'cases': range}
    # print(len(range))

    ftivities = grouped.groupby('case_id')['Activity'].head(100).tolist()
    # print(ftivities)
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



    # TODO NOTES: How to resolve this issue?
    #  0. Try this again but only for one case variant.
    #  1. Iteration 1: Only group by activity -> Rework loops get reduced into
    #  one single activity and are not displayed properly.
    #  This method will work for the majority of flows though. Since we aim to keep rework as low as possible -> DONE
    #  -
    #  2. Iteration 2: Instead of visualising the representation within one case variant, how can we
    #  represent a overview of a case variant comparable with other case variants without going into depth.
    #  -
    #  3. Iteration 3: Rework to collect all cases, including the ones with a rework loop. The arising issue here is
    #  finding a way for groupby to not merge rows together -> groupby with more than 1 column.
    #  Once this is handled the visualisations should be complete and accurate.

    # data = ColumnDataSource(data=data)

    for act in ftivities:
        colors.append("#f9f9f9")
        colors.append(color_dict[act])

    for case in range:
        i = 0
        df = grouped.groupby('case_id').get_group(int(case))
        df = df.groupby(['Activity', 'start_time', 'processing_time', 'waiting_time'], sort=False)

        for k, v in df:
            i += 1

            if k[0] + str(i) in data:
                data[k[0] + str(i) + 'wt'] += [k[3]]
                data[k[0] + str(i)] += [k[2]]
            else:
                data[k[0] + str(i) + 'wt'] = [k[3]]
                data[k[0] + str(i)] = [k[2]]


            # data[k[0] + str(i)] += [v.processing_time]
            # print(i)
            # data.stream()
            # data[' Waiting Time'] = v.waiting_time

    # colors = intersperse(colors, '#f9f9f9')  # Add waiting time between each activity
    # activities = intersperse(activities, " Waiting Time")
    # print(data)
    # print(len(activities))
    # print(len(colors))
    # print(len(ftivities))
    # print(ftivities)

    # -----------------

    # print("colros ups")
    # print(colors)
    # print(len(colors))
    # print("acts")
    # print(activities)
    # print(len(activities))
    #
    # per_case = grouped.groupby('case_id')
    # prev = -1
    # for val in range:
    #     # print(prev)
    #     case_df = per_case.get_group(int(val))
    #     if prev < 0:
    #         prev = case_df['case_id'].drop_duplicates().iloc[0]
    #         cur = prev
    #     if prev != cur:
    #         prev = cur
    #     i = 0
    #
    #     for idx, row in case_df.iterrows():
    #         r = row[['Activity', 'processing_time', 'waiting_time']]
    #         print(row.Activity)
    #         data[' Register Claim'] = row.processing_time
    #         data[' Amend Claim'] = row.waiting_time
    #         i += 1
    #
    #     print(data)
    # print(case_df)
    # print(case_df[['Activity', 'processing_time']])
    # print(case_df[['Activity', 'processing_time']])
    # act = grouped.groupby(['Activity'], level=0, sort=False)
    # act2 = grouped.groupby('case_id', sort=False)
    # i = 0
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
    # print(colors)
    # print(len(activities))
    # print(len(colors))
    # print(data)
    # print(data)

    # TODO REMOVE LAST ENTRY OF EACH LIST SINCE THIS REPRESENTS WAITING TIME THAT DOES NOT EXIST.
    activities = activities[1:]
    colors = colors[1:]

    print(activities)
    print(colors)

    p = figure(y_range=range, width=1800, height=1080, x_range=(-100, 10000), title="Case Variant ID: " + str(name) + " | # of Occurences: " + str(len(range)))
    p.add_tools(HoverTool(tooltips=tooltips))
    p.hbar_stack(activities, y='cases', height=0.9, color=colors, source=ColumnDataSource(data),
                 legend_label=["%s" % x for x in activities])

    p_list.append({'fig': p, 'len': len(range)})

    data = {'activities': range}
    activities = []
    colors = []
    vv+=1
    # if vv == 20:
    #     break
newlist = []
for f in reversed(sorted(p_list, key=lambda d: d['len'])):
    newlist.append(f['fig'])
grid = gridplot(newlist, ncols=1, width=1800, height=600)

show(grid)
