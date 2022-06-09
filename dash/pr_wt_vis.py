import dash_html_components as html
import dash_core_components as dcc
import dash
from preprocessing import transform_data
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('./data/conform_SLA.csv')
df.start_time = pd.to_datetime(df.start_time)
df.end_time = pd.to_datetime(df.end_time)

df = transform_data(df)


df = df.groupby('case_variant').get_group(0)

print(df)

fig = px.histogram(df, x="relative_start_time",
                   color="Activity")


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Turn off reloader if inside Jupyter  # Turn off reloader if inside Jupyter
app.run_server(debug=True)
