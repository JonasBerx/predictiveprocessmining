from bokeh.io import show
from bokeh.models import ColumnDataSource
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
    'Register Claim': '#00ff99',
    'Quick Assessment': '#00ffff',
    'Analyze Claim': '#3399ff',
    'Assess Claim': '#9966ff',
    'Amend Claim': '#00441b',
    'Approve Assessment': '#993366',
    'Amend Assessment': '#ff0000',
    'Finalize Assessment': '#ff9933',
    'Prepare Claim Settlement': '#ffff00',
    'Approve Claim Settlement': '#003366',
    'Amend Claim Settlement': '#669900',
    'Execute Claim Settlement': '#663300',
    'Request Customer Info': '#ff9900'
}

present_activities = df.Activity.drop_duplicates().tolist()
data = {}
variants = list(map(str, df.case_variant.drop_duplicates().tolist()))
data['variants'] = variants
for name, value in df.groupby('case_variant'):
    cases = list(map(int, value['case_id'].drop_duplicates().tolist()))
    print(cases)
    # print(value)
    data[name] = {}

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
counts = [5, 3, 7, 5, 3, 7, 5, 3, 7, 5, 3, 7, 5, 3, 7]
counts2 = [3, 2, 5, 3, 2, 5, 3, 2, 5, 3, 2, 5, 3, 2, 5]
counts3 = [9, 11, 12, 9, 11, 12, 9, 11, 12, 9, 11, 12, 9, 11, 12]
counts4 = [6, 4, 10, 6, 4, 10, 6, 4, 10, 6, 4, 10, 6, 4, 10]

counts5 = [10, 0, 15, 10, 0, 15, 10, 0, 15, 10, 0, 15, 10, 0, 15]
counts6 = [9, -1, 13, 9, -1, 13, 9, -1, 13, 9, -1, 13, 9, -1, 13]

p = figure(y_range=FactorRange(factors=data['variants']), x_range=(0, 20), plot_height=950,
           title="Case variant comparison")

p.hbar(y=data['variants'], right=counts, left=counts2, height=0.8, color="#132456")
p.hbar(y=data['variants'], right=counts3, left=counts4, height=0.8, color="#AAAAAA")
p.hbar(y=data['variants'], right=counts5, left=counts6, height=0.8, color="#666666")

show(p)
