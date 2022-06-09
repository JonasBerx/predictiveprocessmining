# App running at http://127.0.0.1:8050/
# Execute with `python demo_casev_123.py`

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash import *

df = pd.read_csv('./data/conform_SLA.csv')

# Transform into usable data for violin plot
# Step I: Data preprocessing
df.start_time = pd.to_datetime(df.start_time)
df.end_time = pd.to_datetime(df.end_time)


# Step 2: Transformative preprocessing

def calc_activity_process_time(frame):
    """
      Takes a data frame with start_time and end_time column;
      Add new colum with processing time.
    """
    # 1. Calculate difference in date time of row
    diff = (frame.end_time - frame.start_time) / np.timedelta64(1, 'm')

    # 2. In case there is no time. set to 0
    diff[diff.isna()] = pd.Timedelta(0)

    # 3. Populate frame with new column
    frame['processing_time'] = diff

    return frame


def calc_total_process_time_start(frame):
    """
    Takes a data frame with a start_time column;
    Add new colum with cummulative sum for start_time for each case_id.
    """
    # 1. create the difference array from start_time
    r1 = frame.start_time.diff()

    # 2. fill the first value (NaT) with zero
    r1[r1.isna()] = pd.Timedelta(0)

    # 3. convert to seconds and use cumsum -> new column
    frame["relative_start_time"] = np.cumsum(r1.dt.total_seconds().values / 60)

    return frame


def calc_total_process_time_end(frame):
    # 1. calculate cumulative end_time based on processing time and relative start time.
    cprt = frame.relative_start_time + frame.processing_time
    # 2. Create new column with resulted values
    frame["relative_end_time"] = cprt

    return frame


def calc_waiting_time_between(frame):

    wtt = frame.relative_start_time-frame.relative_end_time.shift(1)

    wtt[wtt.isna()] = 0.0

    frame["waiting_time"] = wtt

    return frame


def calc_case_variants(frame):
    """
    This method takes a Pandas Dataframe and returns the same frame but with a case variant identifier
        - Perform equivalent of GROUP_CONCAT to combine all the flows of each case
        - Remove duplicates and reindex
        - Collect all case_id's that follow the case_variant flow
        - Assing case_variant id to the original dataframe
    """
    # Case variant collection
    ddf = frame.groupby('case_id')['Activity'].apply(
        lambda x: ",".join(list(x))).reset_index()
    ddf = ddf.rename(columns={'Activity': 'a_list'})
    ddf = ddf.groupby(ddf.a_list).agg(lambda col: col.tolist()).reset_index()
    ddf['len'] = ddf.case_id.map(len)
    ddf = ddf.sort_values('len', ascending=False)
    ddf = ddf.reset_index()

    # Add case variant index to original dataframe
    frame['case_variant'] = -1

    for jndex, s in ddf.iterrows():
        frame.loc[frame.case_id.isin(s.case_id),
                  'case_variant'] = ddf.loc[jndex].name

    return frame


# Apply transformation functions
df = calc_case_variants(df)
df = calc_activity_process_time(df)
df = df.groupby(df.case_id).apply(calc_total_process_time_start)
df = df.groupby(df.case_id).apply(calc_total_process_time_end)
df = df.groupby(df.case_id).apply(calc_waiting_time_between)

# Visualize waiting times
wdf = df[['case_id', 'case_variant', 'Activity', 'waiting_time']]
wdfs = dict(tuple(wdf.groupby('case_variant')))

test_df1 = df.groupby(df.case_id).get_group(103)
test_df2 = df.groupby(df.case_id).get_group(1)


def generate_violin_plot_waiting_times(df, i):
    fig = px.violin(df, y="waiting_time", color="Activity", x="Activity",
                    title="Case Variant " + str(i), box=True, color_discrete_map={
                        " Register Claim": 'red',
                        " Quick Assessment": 'orange',
                        " Assess Claim": 'yellow',
                        " Finalize Assessment": 'limegreen',
                        " Approve Assessment": 'green',
                        " Prepare Claim Settlement": 'plum',
                        " Approve Claim Settlement": 'cyan',
                        " Execute Claim settlement": 'skyblue',
                        " Analyze Claim": 'blue',
                        " Amend Assessment": 'purple',
                        "t": 'magenta',
                        "q": 'pink'
                    }).update_layout(height=600, width=1600)
    return fig


def generate_diagrams_waiting_time(dict):
    res = [html.H4(children='Data display')]
    for i in range(0, len(dict)):
        dff = dict[i]
        fig = dcc.Graph(
            id="case_variant"+str(i),
            figure=generate_violin_plot_waiting_times(dff, i)
        )
        res.append(fig)

    return res


# Basic violin plot generation function


def generate_violin_plot(df, i):
    fig = px.violin(df, y="processing_time", color="Activity", x="Activity",
                    title="Case Variant " + str(i), box=True, color_discrete_map={
                        " Register Claim": 'red',
                        " Quick Assessment": 'orange',
                        " Assess Claim": 'yellow',
                        " Finalize Assessment": 'limegreen',
                        " Approve Assessment": 'green',
                        " Prepare Claim Settlement": 'plum',
                        " Approve Claim Settlement": 'cyan',
                        " Execute Claim settlement": 'skyblue',
                        " Analyze Claim": 'blue',
                        " Amend Assessment": 'purple',
                        "t": 'magenta',
                        "q": 'pink'
                    }).update_layout(height=600, width=1600)
    return fig


# Make a dict of dataframes, split by case variant
dfs = dict(tuple(df.groupby('case_variant')))


def generate_diagrams(dict):
    res = [html.H4(children='Data display')]
    for i in range(0, len(dict)):
        dff = dict[i]
        fig = dcc.Graph(
            id="case_variant"+str(i),
            figure=generate_violin_plot(dff, i)
        )
        res.append(fig)

    return res


app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


test_page = html.Div([
    dcc.Graph(
        id="test",
        figure=generate_violin_plot(test_df1, 0)
    ),
    dcc.Graph(
        id="test",
        figure=generate_violin_plot(test_df2, 1)
    )
])

index_page = html.Div([
    html.H1("Predictive process mining visualisation demo"),
    dcc.Link('Processing times', href='/pro'),
    html.Br(),
    dcc.Link('Waiting times', href='/wait'),
    html.Br(),

])

page_1_layout = html.Div(
    children=[html.H1("Processing Times visualisation - Violin plot"),
              dcc.Link('Home', href='/'),
              html.Br(),
              dcc.Link('Waiting times', href='/wait'),
              ] + (generate_diagrams(dfs))
)

page_2_layout = html.Div(
    children=[
        html.H1("Waiting Times visualisation - Violin plot"),
        dcc.Link('Home', href='/'),
        html.Br(),
        dcc.Link('Processing times', href='/pro'),
    ] + (generate_diagrams_waiting_time(wdfs))
)

# Update the index


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pro':
        return page_1_layout
    elif pathname == '/wait':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)


# font = {
#     'font-family': 'Arial'
# }

# app.layout = html.Div(
#     style={'font-family': font['font-family']}, children=generate_diagrams_waiting_time(wdfs))
