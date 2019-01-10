import pandas as pd
from sodapy import Socrata
import datetime as dt
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict, Counter
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components


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
    pdatetime_obj = dt.datetime.strptime(idxp, '%Y-%m-%dT%H:%M:%S.%f')
    ptimestamp.append(pdatetime_obj)
inc['date'] = ptimestamp

source = ColumnDataSource(
    data=dict(
        date=inc.date,
        value=inc.value,
    )
)

output_file('PuppyTime.html')
# PLOT FIGURE
    
TOOLS = "hover"

p = figure(plot_width = 1000, plot_height = 600, 
           title = 'Puppy Time Series Data', y_axis_type="linear", x_axis_type='datetime',
           x_axis_label = 'Date', y_axis_label = 'Number of Dogs Born', tools=TOOLS)

p.line(inc.date, inc.value, line_color="blue", line_width = 1)

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([('Value', '@value'),])

show(p)
   
script, div = components(p)
    