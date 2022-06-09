import plotly.express as px
from dash import *

color_discrete_map = {
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
}


def generate_violin_plot_waiting_times(df, i):
    fig = px.violin(df, y="waiting_time", color="Activity", x="Activity",
                    title="Case Variant " + str(i), box=True, color_discrete_map=color_discrete_map).update_layout(height=600, width=1600)
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
