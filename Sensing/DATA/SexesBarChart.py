from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange, HoverTool
from bokeh.plotting import figure
from bokeh.core.properties import value
from bokeh.transform import dodge
from bokeh.embed import components


output_file('GenderBars.html')


fruits = ['M', 'F']
years = ['Crime', 'Puppies']

data = {'fruits' : fruits,
        'Crime'   : [1634, 366],
        'Puppies'   : [1100,900]}

source = ColumnDataSource(data=data)

p = figure(x_range=fruits, y_range=(0, 2000), plot_height=250, title="Ratio of Female to Male Gender",
           toolbar_location=None, tools="")

p.vbar(x=dodge('fruits', -0.25, range=p.x_range), top='Crime', width=0.2, source=source,
       color="#c9d9d3", legend=value("Crime"))

p.vbar(x=dodge('fruits',  0.0,  range=p.x_range), top='Puppies', width=0.2, source=source,
       color="#718dbf", legend=value("Puppies"))


p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"

hover = HoverTool()
hover.tooltips = [
    ("Value", "@Crime / @Puppies")]

hover.mode = 'vline'

p.add_tools(hover)

#show(p)

script, div = components(p)
