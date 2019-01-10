import pandas as pd
from collections import Counter, OrderedDict
from sodapy import Socrata
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import components



client = Socrata("data.cityofnewyork.us", None)
puppy = client.get("5hyw-n69x", limit=2000)
puppy_df = pd.DataFrame.from_records(puppy)

#GROUP DATA AND FIND INSTANCES
breed = puppy_df.groupby("breedname")

bcounts = Counter(puppy_df.breedname, ascending=True)

breed_df2 = pd.DataFrame(bcounts, index=[0])
breed_df = breed_df2.transpose()

breed_df["breed"]= breed_df.index
breed_df.columns = ["count", "breed"]


# FIND TOP 15 VALUES
top = breed_df.nlargest(15, columns=['count'])

count = top['count'].tolist()
breed = list(top.index)
data = top
source = ColumnDataSource(
    data=data)


output_file("PuppyBreedBars.html")

# PLOT
TOOLS = "hover"

p = figure(x_range= breed, plot_height=600, title="Most Popular Dog Breeds",
           toolbar_location=None, tools=TOOLS)

hover = p.select(dict(type=HoverTool))

hover.tooltips = OrderedDict([
    ('Amount', '@top'),
])


p.vbar(x=breed, top=count, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0

p.xaxis.major_label_text_font_size = "8pt"
p.yaxis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.5


show(p)

   
script, div = components(p)
    