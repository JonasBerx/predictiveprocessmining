import numpy as np
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool

from preprocessing import transform_data

df = transform_data()
output_file("layout.html")
# TODO https://docs.bokeh.org/en/latest/docs/user_guide/categorical.html


from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import GnBu5, OrRd5, OrRd9
from bokeh.models import ColumnDataSource

output_file("stacked.html")

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]
activities = df['Activity'].drop_duplicates().tolist()
activities = [" Register Claim", "Waiting Time", " Quick Assessment","Waiting Time", " Finalize Assessment","Waiting Time", " Approve Assessment","Waiting Time",
              " Prepare Claim Settlement"]
print(df)
df = df.groupby('case_variant').get_group(790337521760341813)
c1 = df.groupby('Activity').get_group(" Register Claim")
c2 = df.groupby('Activity').get_group(" Quick Assessment")
c3 = df.groupby('Activity').get_group(" Finalize Assessment")
c4 = df.groupby('Activity').get_group(" Approve Assessment")
c5 = df.groupby('Activity').get_group(" Prepare Claim Settlement")
# 'activities': df['Activity'].drop_duplicates().tolist(),
range = df['case_id'].drop_duplicates().tolist()

colors = ["#025669", "#D3D3D3", "#718dbf", "#D3D3D3", "#e84d60", "#D3D3D3", "#8673A1", "#D3D3D3", "#015D52"]

range = list(map(str, range))
data = {'activities': range,
        " Register Claim": c1.processing_time,
        "Waiting Time": c2.waiting_time,
        " Quick Assessment": c2.processing_time,
        "Waiting Time": c3.waiting_time,
        " Finalize Assessment": c3.processing_time,
        "Waiting Time": c4.waiting_time,
        " Approve Assessment": c4.processing_time,
        "Waiting Time": c5.waiting_time,
        " Prepare Claim Settlement": c5.processing_time,
        }
# print(range)
tooltips = [
            ('Case ID', '@activities'),
            ('Register Claim Duration', '@{ Register Claim}'),
            ('Quick Assessment Duration', '@{ Quick Assessment}'),
            ('Finalize Assessment Duration', '@{ Finalize Assessment}'),
            ('Approve Assessment Duration', '@{ Approve Assessment}'),
            ('Prepare Claim Settlement Duration', '@{ Prepare Claim Settlement}'),
            ('Total Waiting Time', '@{Waiting Time}'),
           ]

p = figure(y_range=range, width=1800, height=900, x_range=(-100, 10000), title="Processing time by case_id")
p.add_tools(HoverTool(tooltips=tooltips))


p.hbar_stack(activities, y='activities', height=0.9, color=colors, source=ColumnDataSource(data),
             legend_label=["%s" % x for x in activities])

p.y_range.range_padding = 0.1
p.ygrid.grid_line_color = None
p.legend.location = "top_right"
p.axis.minor_tick_line_color = None
p.outline_line_color = None

show(p)

# generate some synthetic time series for six different categories
# cats = df['Activity'].drop_duplicates().tolist()
# print(len(cats))
# cats = list("abcdefghj")
# yy = np.random.randn(2000)
# g = np.random.choice(cats, 2000)
# for i, l in enumerate(cats):
#     yy[g == l] += i // 2
# df = pd.DataFrame(dict(score=yy, group=g))


# Try with 1 group
# df = df.groupby('case_variant').get_group(1331063371411158447)

p_list = []


def boxplot(df):
    cats = df['Activity'].drop_duplicates().tolist()
    # find the quartiles and IQR for each category
    groups = df.groupby('Activity')
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group.processing_time > upper.loc[cat]['processing_time']) | (
                group.processing_time < lower.loc[cat]['processing_time'])]['processing_time']

    out = groups.apply(outliers).dropna()

    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = list(out.index.get_level_values(0))
        outy = list(out.values)

    p = figure(title="WIP", background_fill_color="#efefef", x_range=cats)

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper.processing_time = [min([x, y]) for (x, y) in zip(list(qmax.loc[:, 'processing_time']), upper.processing_time)]
    lower.processing_time = [max([x, y]) for (x, y) in zip(list(qmin.loc[:, 'processing_time']), lower.processing_time)]

    # stems
    # p.segment(cats, upper.processing_time, cats, q3.processing_time, line_color="black")
    # p.segment(cats, lower.processing_time, cats, q1.processing_time, line_color="black")

    # boxes
    p.vbar(cats, 0.7, q2.processing_time, q3.processing_time, fill_color="#E08E79", line_color="black")
    p.vbar(cats, 0.7, q1.processing_time, q2.processing_time, fill_color="#3B8686", line_color="black")

    # whiskers (almost-0 height rects simpler than segments)
    # p.rect(cats, lower.processing_time, 0.2, 0.01, line_color="black")
    # p.rect(cats, upper.processing_time, 0.2, 0.01, line_color="black")

    # outliers
    # if not out.empty:
    #     p.circle(outx, outy, size=6, color="#F38630", fill_alpha=0.6)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size = "16px"

    p_list.append(p)
    # show(p)


df = df.groupby('case_variant').apply(boxplot)
print(len(p_list))
grid = gridplot(p_list, ncols=2, width=1800, height=600)
#
show(grid)
