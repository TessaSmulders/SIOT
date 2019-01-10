import numpy as np
import pandas as pd
from bokeh.embed import components
from sodapy import Socrata
import string 
import pandas as pd
from sodapy import Socrata
from bokeh.io import show, output_file
from bokeh.plotting import figure
from collections import Counter, OrderedDict
from bokeh.models import HoverTool, ColumnDataSource


client = Socrata("data.cityofnewyork.us", None)
puppy = client.get("5hyw-n69x", limit=2000)
puppy_df = pd.DataFrame.from_records(puppy)


#GROUP DATA AND FIND INSTANCES
name = puppy_df.groupby("animalname")

counts = Counter(puppy_df.animalname, ascending=True)

name_df2 = pd.DataFrame(counts, index=[0])
name_df = name_df2.transpose()

name_df["name"]= name_df.index

#CLEAN UP DATA
name_df = name_df[~name_df['name'].isin(['ascending'])]

def remove_punctuation(s):
    s = ''.join([i for i in s if i not in frozenset(string.punctuation)])
    return s

name_df['name'] = name_df['name'].apply(remove_punctuation)

name_df.columns = ["count", "name"]



top = name_df.nlargest(10, columns=['count'])

count = top['count'].tolist()

name = list(top.index)

data = top

source = ColumnDataSource(
    data=data)


output_file('PuppyNames.html')

TOOLS = "hover"

p = figure(x_range= name, plot_height=400, title="Most Popular Dog Names",
           toolbar_location=None, tools=TOOLS)


hover = p.select(dict(type=HoverTool))

hover.tooltips = OrderedDict([
    ('Amount', '@top'),
])
print("name", type(name))
print("top", type(count))

p.vbar(x=name, top=count, width=0.9)

p.xgrid.grid_line_color = None
p.y_range.start = 0


p.xaxis.major_label_text_font_size = "8pt"
p.yaxis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 1.5


show(p)
   
script, div = components(p)
    
