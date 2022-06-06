# App running at http://127.0.0.1:8050/
# Execute with `python demo_casev_123.py`

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash import *
from numpy import timedelta64

# df = pd.read_csv('./data/variant_files/case_variant_3.csv')
df = pd.read_csv('./data/conform_SLA.csv')

# Transform into usable data for violin plot
# Step I: Data preprocessing
df.start_time = pd.to_datetime(df.start_time)
df.end_time = pd.to_datetime(df.end_time)

# Step II: Case variant grouping.


def case_variant_clustering(frame):
    flows = []
    flow = []
    # First for loop, splitting rows by case_id
    case_id = df['case_id'][0]
    for ind in df.index:
        if case_id != df['case_id'][ind]:
            case_id = df['case_id'][ind]

            flows.append(flow)
            print(flow)
            flow = [' Register Claim']
        else:
            flow.append(df['Activity'][ind])
    dup_free = []
    for x in flows:
        if x not in dup_free:
            dup_free.append(x)

    # 51 different flows
    print(len(dup_free))

    frame = frame.groupby(frame.case_id, sort=True)
    return frame


print(df.dtypes)
print(case_variant_clustering(df).head(7))


def calc_activity_process_time(frame):
    """
      Takes a data frame with start_time and end_time column;
      Add new colum with processing time.
    """
    # 1. Calculate difference in date time of row
    diff = (frame.end_time - df.start_time) / np.timedelta64(1, 'm')

    # 2. In case there is no time. set to 0
    diff[diff.isna()] = pd.Timedelta(0)

    # 3. Populate frame with new column
    frame['processing_time'] = diff

    return frame


def calc_total_process_time(frame):
    """
    Takes a data frame with a start_time and end_time column;
    Add new colum with cummulative sum for start_time and end_time for each case_id.
    """
    # 1. create the difference array from start_time and end_time
    r1 = frame.start_time.diff()
    r2 = frame.end_time.diff()

    # 2. fill the first value (NaT) with zero
    r1[r1.isna()] = pd.Timedelta(0)
    r2[r2.isna()] = pd.Timedelta(0)

    # 3. convert to seconds and use cumsum -> new column
    frame["relative_start_time"] = np.cumsum(r1.dt.total_seconds().values / 60)
    # TODO end_time does not take into consideration the processing time of the first activity (Register claim)
    frame["relative_end_time"] = np.cumsum(r2.dt.total_seconds().values / 60)

    return frame


# def calc_waiting_time_between(frame):

# Apply transformation functions
df = calc_activity_process_time(df)
df = df.groupby(df.case_id).apply(calc_total_process_time)

# print(df)

by_act = df.groupby(df.Activity)
q = by_act.get_group(' Register Claim')

# TODO Visualize violin plot with case variant 1


def generate_violin_plot(df):
    # Y value will be case variant.
    # range_x=[0, 1000],
    fig = px.violin(df, y="processing_time", color="Activity", x="Activity",
                    title="case variant flows")
    return fig


# TODO Incrementally add case variant 2 / 3


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
font = {
    'font-family': 'Arial'
}

app.layout = html.Div(style={'font-family': font['font-family']}, children=[
    html.H4(children='Data display'),

    dcc.Graph(
        id='example-graph-2',
        figure=generate_violin_plot(df)
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
