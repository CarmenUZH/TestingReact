#!/usr/bin/env python
# coding: utf-8

#Import necessary libraries
import pandas as pd
import numpy as np
from bokeh.io import output_file, show, save,curdoc, output_notebook
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool,FactorRange, NumeralTickFormatter,HBar, DatetimeTickFormatter
from bokeh.models.widgets import Select
from bokeh.layouts import column, row, gridplot
import bokeh.palettes as bp # uncomment it if you need special colors that are pre-defined
import datetime as dt
from math import pi
from bokeh.layouts import gridplot
from bokeh.models import BoxSelectTool, LassoSelectTool


# ----- PART1: SCATTER PLOT ----------

#Data Pre-processing
#Read data
df = pd.read_csv('train.csv')


np.random.seed(10)

#Remove some of the data because there is too much :/ (Do not touch this part.)
remove_n = 1455000
drop_indices = np.random.choice(df.index, remove_n, replace=False)
df = df.drop(drop_indices)


#Drop the rows that has larger trip_duration value than 2000. They are outliers in our case.
df = ...


#For the scatterplot, in the x-axis we need the dates. So,extract dates from the dataframe, we will use the 'pickup_datetime' column.
df['pickup_datetime'] = ...
df['dates'] = ...

#Color operations
    # Vendor_id will be color coded. Append different color to different vendor_id. 
    # Color column is already created for you and filled with a default color. 

color = list()
for i in range(len(df.index)):
    color.append("#A9A9A9")

df['color'] = color

#Assign colors according to vendor_id
for idx in df.index:
    ...

#Replace vendor_id -> 1,2 with "vendor_1","vendor_2"
df['vendor_id'] = ...


#Create your dataframe for the scatterplot, and sort it by the "dates" column
#Hint: What you need for the scatterplot dataframe are "trip_duration", "dates", "vendor_id", "color", and "passenger_count". 
#Extract these necessary information from the main dataframe.

df_scatterplot = ...


#Convert datetime to string
df_scatterplot['dates'] = df_scatterplot['dates'].apply(lambda x: x.strftime("%Y-%m-%d"))

#Create the ColumnDataSource by first creating a dictionary
data = {
        ...
    }
source_scatter = ColumnDataSource(data)

#Set your x-range
#Hint: Your x-range should contain all of the dates.

x_Range = ...

#For interaction we will use "Lasso Selection" and "Box Selection" tools.
TOOLS="lasso_select, box_select, reset"

#Create figure for scatterplot.
p = figure(tools=TOOLS, plot_width=3000, plot_height=900,
           toolbar_location="above",x_range = x_Range,
           title="NYC Taxi Traffic")

p.yaxis.axis_label = "Trip Duration (seconds)"
p.xaxis.axis_label = "Dates"
p.xaxis.major_label_orientation = pi/4
p.xaxis.major_label_text_font_size = '8px'
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.sizing_mode = "stretch_both"
p.select(LassoSelectTool).select_every_mousemove = False
p.select(BoxSelectTool).select_every_mousemove = False

#Create hover tool.
#Hover tool must show : Date,Trip duration,number of passengers and vendor_id
hover = HoverTool(tooltips = [
    ...
])
p.add_tools(hover)

#Create the scatterplot, be aware that the size of the circles should encode the number of passengers.
scatter = p.scatter(...)

# ------------ PART2: HISTOGRAM OF TRIP DURATION ----------------

# Create the  histogram
# Reference Links:
    #https://www.tutorialspoint.com/numpy/numpy_histogram_using_matplotlib.htm 
    #https://www.geeksforgeeks.org/numpy-histogram-method-in-python/
    #https://numpy.org/doc/stable/reference/generated/numpy.histogram.html 

# Hint:
# First you need to extract the trip duration data from the dataframe, then compute the histogram for the whole data, with the bins=20
# Second you need to figure out the way to create the histogram only for the selected data,
# And since the selected data are from two vendors, you should plot stacked bar chart for the selected data for two different vendors.
hhist, hedges = np.histogram(...)

hzeros = np.zeros(len(hedges)-1)
hmax = max(hhist)*1.1

LINE_ARGS1 = dict(color="#ffbdbd", line_color=None)
LINE_ARGS2 = dict(color="#d9f5d9", line_color=None)

ph = figure(title="Histogram", tools='', background_fill_color="#fafafa", plot_width=1500, plot_height=200, x_range=p.y_range, y_range=(0, hmax))
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4

# Use ph.quad() for creating the bins. Please read the reference link carefully. 
# Reference links:
    #https://docs.bokeh.org/en/latest/docs/gallery/histogram.html

ph.quad(...)
ph.y_range.start = 0
ph.yaxis.axis_label = "Number of Trips"
ph.xaxis.axis_label = "Trip Duration"

# Create two more histogram quads for selected data. 
# These two quads will be manipulated by the selection tools. When we select data from the scatter plot, we want histogram to be highlighted with the parts that
# corresponds to our data points. Therefore, we need two more quads to indicate the highlighted area. The color will be the same but we will use the alpha value = 0.5 

hh1 = ph.quad(..., alpha=0.5,**LINE_ARGS1)
hh2 = ph.quad(..., alpha=0.5,**LINE_ARGS2)

# ---------------- PART3: LASSO AND BOX TOOLS SELECTION WIDGET -----------------

# Implement the update function that will be triggered when the lasso or box selection tool is used.
def update(attr, old, new):
    nds = new  # index of the data that are selected
    ...


# Bind the update function to lasso tool and data
scatter.data_source.selected.on_change('indices', update)

# use curdoc to add your widgets to the documents
layout = column(p, row(ph))
curdoc().add_root(layout)