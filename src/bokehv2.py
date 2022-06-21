import numpy as np
import pandas as pd

from bokeh.layouts import gridplot
from bokeh.io import output_file, show
from bokeh.plotting import figure

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.palettes import GnBu5, OrRd5, OrRd9
from bokeh.models import ColumnDataSource

from preprocessing import transform_data

df = transform_data()
output_file("layout.html")