# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc


df = pd.read_csv('./data/Claims_Management_Simplified.csv')

font = {
    'font-family': 'Arial'
}


def generate_table(df):
    fig = dash_table.DataTable(df.to_dict('records'), [
        {"name": i, "id": i} for i in df.columns], id='tbl')
    return fig


def generate_violin_plot(df):
    fig = px.violin(df, y="Resource", color="Activity")
    return fig


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(style={'font-family': font['font-family']}, children=[
    html.H4(children='Data display'),

    dcc.Graph(
        id='example-graph-2',
        figure=generate_violin_plot(df)
    ),
    generate_table(df),


])

if __name__ == '__main__':
    app.run_server(debug=True)
