import base64
from io import BytesIO

from flask import Flask
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sb

from preprocessing import transform_data

app = Flask(__name__)

# df = transform_data()
# total_cases = len(df.drop_duplicates('case_id'))
#
# # Make a dict of dataframes, split by case variant
# dfs = dict(tuple(df.groupby('case_variant')))


def get_stats(frame):
    res = frame.drop_duplicates('case_id')
    return len(res)


def generate_box_plots(df, i, total, total_cases):
    box = sb.boxplot(data=df, y="processing_time", x="Activity", whis=0, fliersize=0)
    percent = total / total_cases * 100
    percent = '{:.2f}'.format(percent)
    plt.title = "Case Variant " + str(i) + " | Occurrences: " + str(total) + " | " + str(percent) + "%"

    return box


def generate_box(dict, total_cases):
    res_tup = []
    i = 1

    for value in dict.values():
        total = get_stats(value)
        dff = value
        fig = generate_box_plots(dff, i, total, total_cases)
        tup = (total, fig)
        res_tup.append(tup)
        i += 1
    res_tup.sort(key=lambda t: t[0], reverse=True)
    res = []
    for (i, j) in res_tup:
        res.append(j)
    return res


@app.route("/")
def out():
    df = transform_data()
    total_cases = len(df.drop_duplicates('case_id'))

    # Make a dict of dataframes, split by case variant
    dfs = dict(tuple(df.groupby('case_variant')))

    figs = generate_box(dfs, total_cases)
    print(figs)
    res = []
    out = ''
    buf = BytesIO()
    for k in figs:
        fig = k.get_figure()
        fig.savefig(buf)
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        out += f"<p><img src='data:image/png;base64,{data}'/></p>"
        # break
    # print(out)
    return out
