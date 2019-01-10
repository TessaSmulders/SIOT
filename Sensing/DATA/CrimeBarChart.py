import pandas as pd
from sodapy import Socrata
from bokeh.io import show, output_file
from bokeh.plotting import figure
from collections import Counter, OrderedDict
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import components


# DATA FROM API AND PLACE INTO DATAFRAME
client = Socrata("data.cityofnewyork.us", None)
crime = client.get("999i-ek3f", limit=2000)
crime_df = pd.DataFrame.from_records(crime)


output_file("CrimeBars.html")

counts = Counter(crime_df.pd_desc)

uniquevals = pd.DataFrame(counts, index=[0])
uv = uniquevals.transpose()

label = list(map(str,(set(crime_df.pd_desc))))
uv['label']= label 
uv.columns = ["num", "label"]



num = list(uv.num)
label = list(uv.index)


top = uv.nlargest(40, columns=['num'])

top = top.replace('nan', 'ASSAULT')


num = list(top.num)
label = list(top.index)

source = ColumnDataSource(
    data=dict(
        num=num,
        label=label,
    )
)


TOOLS = "hover"

p = figure(x_range= top['label'], plot_height=1000, title="Most Common Incidents",
           toolbar_location=None, tools=TOOLS)


hover = p.select(dict(type=HoverTool))

hover.tooltips = OrderedDict([
    ('Amount', '@top'),
])


p.vbar(x=top.label, top=top.num, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0


p.xaxis.major_label_text_font_size = "8pt"
p.yaxis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.5


show(p)

script, div = components(p)
