import dash_bootstrap_components as dbc
import pandas as pd
from preprocessing import transform_data
from visualisation import generate_diagrams, generate_diagrams_waiting_time, generate_box
from dash import *

df = transform_data()
total_cases = len(df.drop_duplicates('case_id'))

# Visualize waiting times
wdf = df[['case_id', 'case_variant', 'Activity', 'waiting_time']]
wdfs = dict(tuple(wdf.groupby('case_variant')))

# Make a dict of dataframes, split by case variant
dfs = dict(tuple(df.groupby('case_variant')))

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.H1("Predictive process mining visualisation demo"),
    dcc.Link('Processing times', href='/pro'),
    html.Br(),
    dcc.Link('Waiting times', href='/wait'),
    html.Br(),
    dcc.Link('Box plots', href='/box'),
    html.Br(),

])

page_1_layout = html.Div(
    children=[html.H1("Processing Times visualisation - Violin plot"),
              dcc.Link('Home', href='/'),
              html.Br(),
              dcc.Link('Waiting times', href='/wait'),
              ] + (generate_diagrams(dfs, total_cases))
)

page_2_layout = html.Div(
    children=[
                 html.H1("Waiting Times visualisation - Violin plot"),
                 dcc.Link('Home', href='/'),
                 html.Br(),
                 dcc.Link('Processing times', href='/pro'),
             ] + (generate_diagrams_waiting_time(wdfs))
)

page_3_layout = html.Div(
    children=[
                 html.H1("Box plots (Q1-Q2-Q3)"),
                 dcc.Link('Home', href='/'),
             ] + (generate_box(dfs, total_cases))
)


# Update the index


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pro':
        return page_1_layout
    elif pathname == '/wait':
        return page_2_layout
    elif pathname == '/box':
        return page_3_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
