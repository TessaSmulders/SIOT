import pandas as pd
import numpy as np
import datetime
from collections import OrderedDict
from bokeh.models import HoverTool, BasicTicker, ColumnDataSource, PrintfTickFormatter
from bokeh.embed import components
from bokeh.io import show, output_file
from bokeh.plotting import figure



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


weeks = list(data.index)
days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

max_count = realraw["count"].max()
day_of_week = []
week = []
color = []
crimes = []
for w in weeks:
    for idx, day in enumerate(days):
        day_of_week.append(day)
        week.append(w)
        count = data.loc[w][idx]
        crimes.append(count)
        avecount = int(255-(count/max_count)*255)
        color.append("#%02x%02x%02x" % (255, avecount, avecount))

source = ColumnDataSource(
    data=dict(
        day_of_week=day_of_week,
        week=week,
        color=color,
        crimes=crimes,
    )
)

output_file('NYCcrimesHeatmap.html')

TOOLS = "hover"

p=figure(
    title='Number of crimes per day from 2013-2015', 
    x_range=weeks, 
    y_range=list(reversed(days)),
    tools=TOOLS,
    )
p.plot_width=1000
p.plot_height = 400
p.toolbar_location='left'

p.rect(x="week", y="day_of_week", width=1, height=1, source=source, fill_color="color", line_color=None)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.xaxis.major_label_text_font_size = "4pt"
p.yaxis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.5


hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('crimes', '@crimes'), ('week', '@week'),
])

#p.toolbar.autohide = True

show(p) 

script, div = components(p)