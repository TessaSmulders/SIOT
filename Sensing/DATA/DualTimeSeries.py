import pandas as pd
import numpy as np
from sodapy import Socrata
import datetime
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict, Counter
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components


# COLLECT DATA AND WRITE TO DATAFRAME
client = Socrata("data.cityofnewyork.us", None)

puppy = client.get("5hyw-n69x", limit=2000)
puppy_df = pd.DataFrame.from_records(puppy).sort_values(['animalbirth'], ascending=True)


# CALCULATE INCIDENT NUMBERS
counts = Counter(puppy_df.animalbirth)
incident = pd.DataFrame(counts, index=[0])
inc = incident.transpose()

inc['date']= inc.index
inc.columns = ["value", "date"]


# CONVERT DATES TO TIMESTAMP
ptimestamp=[]
for idxp in inc['date']:
    pdatetime_obj = datetime.datetime.strptime(idxp, '%Y-%m-%dT%H:%M:%S.%f')
    ptimestamp.append(pdatetime_obj)
inc['date'] = ptimestamp
 

#MATCH CRIME DATA TIMEFRAME
inc = inc[inc.date > '2012-12-01']
inc = inc[inc.date <= '2015-12-01']

    
## CRIME DATAFRAME
query = ("https://data.cityofnewyork.us/resource/999i-ek3f.json?"
    "$group=date"
    "&$select=date_trunc_ymd(arrest_date)%20AS%20date%2C%20count(*)"
    "&$order=date")
raw_data = pd.read_json(query)

raw_data['day_of_week'] = [date.dayofweek for date in raw_data["date"]]
raw_data['week'] = [(date - datetime.timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in raw_data["date"]]

realraw = raw_data[raw_data.week != '2016-08-31']

data = realraw.pivot(index='week', columns='day_of_week', values='count')
data = data.fillna(value=0)

weeks = list(data.index)
days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

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


cinc = pd.DataFrame(crimes)
cinc['cdate']=realraw['date']
cinc.columns = ["value", "date"]


## NORMALIZE DATA

n_puppies = (inc['value'] - np.mean(inc['value']))/np.std(inc['value'])
n_crimes = (cinc['value'] - np.mean(cinc['value']))/np.std(cinc['value'])


source = ColumnDataSource(
    data=dict(
        date=inc.date,
        value=inc.value,
        day_of_week=day_of_week,
        week=week,
        crimes=crimes,
    )
)
    
output_file('ComparisonTime.html')


# PLOT FIGURE
    
TOOLS = "hover"

p = figure(plot_width = 1000, plot_height = 600, 
           title = 'Comparison Time Series Data', y_axis_type="linear", x_axis_type='datetime',
           x_axis_label = 'Date', y_axis_label = 'Value', tools=TOOLS)

p.line(inc.date, n_puppies, line_color="red", line_width = 2, legend = 'Puppies')
p.line(realraw['date'], n_crimes, line_color="blue", line_width = 1, legend = 'Crime')

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([('Value', '@top'),])

show(p)
    
    
script, div = components(p)
    