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

def get_stats(frame):
    res = frame.drop_duplicates('case_id')
    return len(res)


def generate_violin_plot_waiting_times(df, i, total):
    fig = px.violin(df, y="waiting_time", color="Activity", x="Activity",
                    title="Case Variant " + str(i) + " Occurrences: " + str(total), box=True,
                    color_discrete_map=color_discrete_map).update_layout(height=600, width=1600)
    return fig


def generate_diagrams_waiting_time(dict):
    res = [html.H4(children='Data display')]
    for key, value in dict.items():
        total = get_stats(value)
        dff = value
        fig = dcc.Graph(
            id="case_variant"+str(key),
            figure=generate_violin_plot_waiting_times(dff, key, total)
        )
        res.append(fig)

    return res


def generate_violin_plot(df, i, total, total_cases):
    percent = total/total_cases * 100
    percent = '{:.2f}'.format(percent)
    fig = px.violin(df, y="processing_time", color="Activity", x="Activity",
                    title="Case Variant " + str(i) + " | Occurrences: " + str(total) + " | " + str(percent) + "%", box=True,
                    color_discrete_map={
                        " Register Claim": 'orange',
                        " Quick Assessment": 'yellow',
                        " Assess Claim": 'green',
                        " Finalize Assessment": 'purple',
                        " Approve Assessment": 'darkgrey',
                        " Prepare Claim Settlement": 'mediumvioletred',
                        " Approve Claim Settlement": 'cyan',
                        " Execute Claim settlement": 'skyblue',
                        " Analyze Claim": 'grey',
                        " Amend Assessment": 'coral',
                        "t": 'magenta',
                        "q": 'pink'
                    }).update_layout(height=600, width=1600)
    return fig


def generate_diagrams(dict, total_cases):
    res_tup = []
    res = [html.H4(children='Data display - Total cases: ' + str(total_cases))]
    for key, value in dict.items():
        total = get_stats(value)
        dff = value
        fig = dcc.Graph(
            id="case_variant"+str(key),
            figure=generate_violin_plot(dff, key, total, total_cases)
        )
        # l.append(fig)
        tup = (total, fig)
        res_tup.append(tup)

    # print(res_tup)
    res_tup.sort(key=lambda t: t[0], reverse=True)
    for (i, j) in res_tup:
        res.append(j)
    # print(res_dict)
    # print(len(res_dict))
    # res.append(l)
    return res
