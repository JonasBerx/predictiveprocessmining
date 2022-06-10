from dash import *
from preprocessing import transform_data
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

plt.style.use('_mpl-gallery')

df = pd.read_csv('./data/conform_SLA.csv')
df.start_time = pd.to_datetime(df.start_time)
df.end_time = pd.to_datetime(df.end_time)

df = transform_data(df)


df = df.groupby('case_variant').get_group(0)
l = []
act = [" Register Claim", " Analyze Claim", " Assess Claim", " Approve Assessment",
       " Approve Claim Settlement", " Execute Claim Settlement", " Finalize Assessment", " Prepare Claim Settlement"]


for f in act:
    l.append(df.groupby('Activity').get_group(f)['relative_start_time'])

prt = df['processing_time']
prtt = df['relative_start_time']
print(df)

# df = df.groupby('Activity')
# df = df['relative_start_time']


fig, ax = plt.subplots()
colors = ['orange', 'mediumvioletred', 'green', 'whitesmoke', 'darkgrey',
          'cyan', 'skyblue', 'purple']

ax.eventplot(l, orientation="horizontal", colors=colors, linewidth=1)

plt.show()

# TODO Make this thing work with a loop for each case variant + port towards Dash for web visualisation.
# TODO Find a way to combine the data from one event plot into one row. With different colors for each Activity.
# TODO Make it so that outliers get remo


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Turn off reloader if inside Jupyter  # Turn off reloader if inside Jupyter
app.run_server(debug=True)
