import pandas as pd
import numpy as np

import datetime
 
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file
#from bkcharts import TimeSeries

 

query = ("https://data.cityofnewyork.us/resource/999i-ek3f.json?"
    "$group=date"
    "&$select=date_trunc_ymd(arrest_date)%20AS%20date%2C%20count(*)"
    "&$order=date")
raw_data = pd.read_json(query)

raw_data['day_of_week'] = [date.dayofweek for date in raw_data["date"]]
raw_data['week'] = [(date - datetime.timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in raw_data["date"]]


realraw = raw_data[raw_data.week != '2012-12-31']

data = realraw.pivot(index='week', columns='day_of_week', values='count')
data = data.fillna(value=0)

## Get our "weeks" and "days"

weeks = list(data.index)
days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

## Set up the data for plotting. We will need to have values for every
## pair of year/month names. Map the rate to a color.

max_count = realraw["count"].max()
day_of_week = []
week = []
crimes = []
for w in weeks:
    for idx, day in enumerate(days):
        day_of_week.append(day)
        week.append(w)
        count = data.loc[w][idx]
        crimes.append(count)

source = ColumnDataSource(
    data=dict(
        day_of_week=day_of_week,
        week=week,
        crimes=crimes,
    )
)


# PLOT FIGURE
    
TOOLS = "hover"

p = figure(plot_width = 1000, plot_height = 600, 
           title = 'Crime Statistics over Time', y_axis_type="linear", x_axis_type='datetime',
           x_axis_label = 'Date', y_axis_label = 'Number of Incidents', tools=TOOLS)

p.line(realraw['date'], crimes, line_color="blue", line_width = 1)

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([('Crimes', '@crimes'),])

show(p)
