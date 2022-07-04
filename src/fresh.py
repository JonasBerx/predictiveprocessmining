import sys

from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.plotting import figure
import random

from bokeh.transform import jitter

from preprocessing import transform_data

# Preprocessing and only retain case variants that have more than 3 occurrences
df = transform_data()
all_activities = df.Activity.drop_duplicates().tolist()
df = df.groupby('case_variant').filter(lambda x: x['case_id'].nunique() > 5)

# TODO 1: Color Dictionary for activities
# TODO 2: Get Q1 and Q3 for each activity in each case variant
# TODO 3: Fill all unknown activities (not present in variant x with 0's)
# TODO 4: Loop HBAR

"""
    COLORS FOR ACTIVITIES
    ---------------------
    #00ff99 : REGISTER CLAIM
    #00ffff : QUICK ASSESSMENT
    #3399ff : ANALYZE CLAIM
    #9966ff : ASSESS CLAIM
    #ff00ff : AMEND CLAIM
    #993366 : APPROVE ASSESSMENT
    #ff0000 : AMEND ASSESSMENT
    #ff9933 : FINALIZE ASSESSMENT
    #ffff00 : PREPARE CLAIM SETTLEMENT
    #003366 : APPROVE CLAIM SETTLEMENT
    #669900 : AMEND CLAIM SETTLEMENT
    #663300 : EXECUTE CLAIM SETTLEMENT
    #ff9900 : REQUEST CUSTOMER INFO
"""

color_dict = {
    'Register Claim': (0, 255, 153, 0.4),
    'Quick Assessment': (0, 255, 255, 0.4),
    'Analyze Claim': (51, 153, 255, 0.4),
    'Assess Claim': (153, 102, 255, 0.4),
    'Amend Claim': (0, 68, 27, 0.4),
    'Approve Assessment': (153, 51, 102, 0.4),
    'Amend Assessment': (255, 0, 0, 0.4),
    'Finalize Assessment': (255, 153, 51, 0.4),
    'Prepare Claim Settlement': (255, 255, 0, 0.4),
    'Approve Claim Settlement': (0, 51, 102, 0.4),
    'Amend Claim Settlement': (102, 153, 0, 0.4),
    'Execute Claim Settlement': (102, 51, 0, 0.4),
    'Request Customer Info': (255, 153, 0, 0.4),
}

present_activities = df.Activity.drop_duplicates().tolist()
data = {}
variants = list(map(str, df.case_variant.drop_duplicates().tolist()))
data['variants'] = variants

print(present_activities)

for act in present_activities:
    data[act + "_START"] = []
    data[act + "_END"] = []

min_val = sys.maxsize
max_val = -sys.maxsize - 1

absolute_max = 0

for name, value in df.groupby('case_variant'):
    cases = list(map(int, value['case_id'].drop_duplicates().tolist()))
    cv_activities = value['Activity'].drop_duplicates().tolist()
    print(cv_activities)
    # print(cases)
    # print(value)
    for act, info in value.groupby(['Activity'], sort=False):
        print(info.relative_start_time.quantile([.25, .75]))
        print(info.relative_start_time.mean())
        print(info.relative_end_time.quantile([.25, .75]))
        print(info.relative_end_time.mean())
        # APPROACH 1: MEAN
        data[act + "_START"].append(info.relative_start_time.mean())
        data[act + "_END"].append(info.relative_end_time.mean())

        # APPROACH 2: MEDIAN
        # data[act + "_START"].append(info.relative_start_time.median())
        # data[act + "_END"].append(info.relative_end_time.median())


        # APPROACH 3: Define min and max value for Activity
        # if info.relative_start_time.min() < min_val:
        #     max_val = info.relative_start_time.min()
        # if info.relative_end_time.max() > max_val:
        #     min_val = info.relative_end_time.max()
        #
        # data[act + "_START"].append(min_val)
        # data[act + "_END"].append(max_val)

        if info.relative_end_time.max() > absolute_max:
            absolute_max = info.relative_end_time.max()

    for act2 in present_activities:
        if act2 not in cv_activities:
            data[act2 + "_START"].append(-1)
            data[act2 + "_END"].append(-1)

    # for case in cases:
    #     print(case)
    #
    # for act, info in value.groupby(['Activity', 'case_id', 'relative_start_time'], sort=False):
    #     print(info)

print(data)
# --------- #
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.models import FactorRange

case_v = ['1', '2', '3']
# counts = [5, 3, 7, 5, 3]  # 7, 5, 3, 7, 5, 3, 7, 5, 3, 7]
# counts2 = [3, 2, 5, 3, 2]  # 5, 3, 2, 5, 3, 2, 5, 3, 2, 5]
# counts3 = [9, 11, 12, 9, 11]  # 12, 9, 11, 12, 9, 11, 12, 9, 11, 12]
# counts4 = [6, 4, 10, 6, 4]  # 10, 6, 4, 10, 6, 4, 10, 6, 4, 10]
#
# counts5 = [10, 0, 15, 10, 0]  # 15, 10, 0, 15, 10, 0, 15, 10, 0, 15]
# counts6 = [9, -1, 13, 9, -1]  # 13, 9, -1, 13, 9, -1, 13, 9, -1, 13]

# Waiting time calcs


p = figure(y_range=FactorRange(factors=data['variants']), x_range=(0, 20000), plot_height=700, plot_width=1600,
           title="Case variant comparison")

for act in present_activities:
    p.hbar(y=data['variants'], right=data[act + "_END"], left=data[act + "_START"], height=0.8, color=color_dict[act],
           legend_label=act)
p.hbar(y=data['variants'], right=absolute_max, left=0, height=0.8, color=(60, 60, 60, 0.05), legend_label="Waiting Time")
# tooltips = [('Case Variant', '@variant')]

# p.add_tools(HoverTool())

div = Div(text="""Some information regarding the dataset:""",
width=200, height=100)

# show(div)

# p.hbar(y=data['variants'], right=counts, left=counts2, height=0.8, color="#132456")
# p.hbar(y=data['variants'], right=counts3, left=counts4, height=0.8, color="#AAAAAA")
# p.hbar(y=data['variants'], right=counts5, left=counts6, height=0.8, color="#666666")

show(p)
