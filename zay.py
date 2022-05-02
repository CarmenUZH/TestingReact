#!/usr/bin/env python
# coding: utf-8

# Import necessary libraries
import pandas as pd
import numpy as np
from bokeh.io import output_file, show, save, curdoc, output_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange, NumeralTickFormatter, HBar, DatetimeTickFormatter
from bokeh.models.widgets import Select
from bokeh.layouts import column, row, gridplot
import bokeh.palettes as bp  # uncomment it if you need special colors that are pre-defined
import datetime as dt
from math import pi
from bokeh.layouts import gridplot
from bokeh.models import BoxSelectTool, LassoSelectTool

#By Carmen Kirchdorfer - 20-720-132
# ----- PART1: SCATTER PLOT ----------

# Data Pre-processing
# Read data
df = pd.read_csv('data.csv')  # changed the name of the file

np.random.seed(10)

# Removing some of the data
remove_n = 1455000
drop_indices = np.random.choice(df.index, remove_n, replace=False)
df = df.drop(drop_indices)

# Dropping the rows that have a trip_duration value that is larger than 2000. They are outliers in our case.
df = df.drop(df[df['trip_duration'] > 2000].index)

#extracting the data we need for the scatterplot
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'], errors='coerce', dayfirst=False, yearfirst=False,
                                       utc=None, format=None, exact=True, unit=None, infer_datetime_format=False,
                                       origin='unix', cache=True)
df['dates'] = df['pickup_datetime'].apply(lambda x: x.date())

# Color operations
# Color-coding based on vendor_id

color = list()
for i in range(len(df.index)):
    color.append("#A9A9A9")

df['color'] = color

# Asigning colours
colors = ['#FF0000', '#32CD32']
for idx in df.index:
    if df.at[idx, 'vendor_id'] == 1:
        df.at[idx, 'color'] = colors[0]
    else:
        df.at[idx, 'color'] = colors[1]

# Replacing the integer values of vendor_id  with strings "vendor_1" or "vendor_2"
df['vendor_id'] = df['vendor_id'].astype(str)
for idx in df.index:
    if df.at[idx, 'vendor_id'] == "1":
        df.at[idx, 'vendor_id'] = "vendor_1"
    else:
        df.at[idx, 'vendor_id'] = "vendor_2"

# Creating the dataframe we need for the scatterplot and sorting by date

df_scatterplot = df[['dates', 'trip_duration', 'vendor_id', 'color', 'passenger_count']].copy()
df_scatterplot.sort_values('dates', inplace=True)

# Converting datetime to string
df_scatterplot['dates'] = df_scatterplot['dates'].apply(lambda x: x.strftime("%Y-%m-%d"))

# Creating the ColumnDataSource by first creating a dictionary
data = {
    'Vendor': list(df_scatterplot['vendor_id']),
    'TripDuration': list(df_scatterplot['trip_duration']),
    'NumOfPass': list(df_scatterplot['passenger_count']),
    'Dates': list(df_scatterplot['dates']),
    'Color': list(df_scatterplot['color'])
}
source_scatter = ColumnDataSource(data=data)

# Setting x-range as unique dates
x_Range = list(df_scatterplot['dates'].unique())

# For interaction we will use "Lasso Selection" and "Box Selection" tools.
TOOLS = "lasso_select, box_select, reset"

# Creating the figure for the scatterplot.
p = figure(tools=TOOLS, plot_width=3000, plot_height=900,
           toolbar_location="above", x_range=x_Range,
           title="NYC Taxi Traffic")

p.yaxis.axis_label = "Trip Duration (seconds)"
p.xaxis.axis_label = "Dates"
p.xaxis.major_label_orientation = pi / 4
p.xaxis.major_label_text_font_size = '8px'
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.sizing_mode = "stretch_both"
p.select(LassoSelectTool).select_every_mousemove = False
p.select(BoxSelectTool).select_every_mousemove = False

# Creating hover tool.
hover = HoverTool(tooltips=[
    ('Date', '@Dates'),
    ('Number of Passengers', '@NumOfPass'),
    ('Vendor', '@Vendor')
])
p.add_tools(hover)

# Creating the scatterplot
scatter = p.scatter('Dates', 'TripDuration',
                    source=source_scatter,
                    color='Color',
                    size='NumOfPass', #make the circlesize relative to the number of passengers
                    legend='Vendor' #Adding a legend :)
                    )

# ------------ PART2: HISTOGRAM OF TRIP DURATION ----------------

# Creating the histogram
a = np.array(df_scatterplot['trip_duration'])
hhist, hedges = np.histogram(a, bins=20, range=None, normed=None, weights=None, density=None)

hzeros = np.zeros(len(hedges) - 1)
hmax = max(hhist) * 1.1

LINE_ARGS1 = dict(color="#ffbdbd", line_color=None)
LINE_ARGS2 = dict(color="#d9f5d9", line_color=None)

ph = figure(title="Histogram", tools='', background_fill_color="#fafafa", plot_width=1500, plot_height=200,
            x_range=p.y_range, y_range=(0, hmax))
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi / 4

#making the "outline" quad
ph.quad(top=hhist, bottom=0, left=hedges[:-1], right=hedges[1:], fill_color='white')
ph.y_range.start = 0
ph.yaxis.axis_label = "Number of Trips"
ph.xaxis.axis_label = "Trip Duration"

# Creating two more histogram quads for selected data.
hh1 = ph.quad(top=hzeros, bottom=0, left=hedges[:-1], right=hedges[1:],  alpha=0.5, **LINE_ARGS1) #red
hh2 = ph.quad(top=hzeros, bottom=hzeros, left=hedges[:-1], right=hedges[1:], alpha=0.5, **LINE_ARGS2) #green

#updates the two quads whenever lasso tool gets triggered
def update(attr, old, new):
    nds = new  # index of the data that are selected
    eins = np.array([])
    zwei = np.array([])
    for idx in nds:
        if df_scatterplot['vendor_id'].iloc[idx] == "vendor_1":
            eins = np.append(eins,df_scatterplot['trip_duration'].iloc[idx])
        else:
            zwei = np.append(zwei,df_scatterplot['trip_duration'].iloc[idx])

    if len(nds) == 0:
        hhist1, hhist2 = hzeros, hzeros
    else:
        hhist1, _ = np.histogram(eins, bins=hedges)
        hhist2, _ = np.histogram(zwei, bins=hedges)


    hh1.data_source.data["top"] = hhist1
    hh2.data_source.data["bottom"] = hhist1
    hh2.data_source.data["top"] = np.add(hhist2,  hhist1)

# Binds the update function to lasso tool and data
scatter.data_source.selected.on_change('indices', update)

# using curdoc to add my widgets to the documents
layout = column(p, row(ph))
curdoc().add_root(layout)

# save result as html
output_file("ex3_20720132.html")
show(layout)

#to use: bokeh serve --show (filename)