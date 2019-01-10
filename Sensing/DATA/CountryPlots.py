import pandas as pd
from sodapy import Socrata
import pyproj 
import datetime as dt
from uszipcode import SearchEngine
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components


# DATA FROM API AND PLACE INTO DATAFRAME
client = Socrata("data.cityofnewyork.us", None)
crime = client.get("999i-ek3f", limit=2000)
crime_df = pd.DataFrame.from_records(crime)

puppy = client.get("5hyw-n69x", limit=2000)
puppy_df = pd.DataFrame.from_records(puppy).sort_values(['animalbirth'], ascending=True)

# CONVERT DATES TO TIMESTAMP
ptimestamp=[]
for idxp in puppy_df['animalbirth']:
    pdatetime_obj = dt.datetime.strptime(idxp, '%Y-%m-%dT%H:%M:%S.%f')
    ptimestamp.append(pdatetime_obj)
puppy_df['timestamp'] = ptimestamp

ctimestamp=[]
for idxc in crime_df['arrest_date']:
    cdatetime_obj = dt.datetime.strptime(idxc, '%Y-%m-%dT%H:%M:%S.%f')
    ctimestamp.append(cdatetime_obj)
crime_df['timestamp'] = ctimestamp

# CONVERT CRIME DATA TO WEB MERCATO
inProj = pyproj.Proj(init='epsg:4326')
outProj = pyproj.Proj(init='epsg:3857')

def convertCoords(row):
    x2,y2 = pyproj.transform(inProj,outProj,row['longitude'],row['latitude'])
    return pd.Series({'newLong':x2,'newLat':y2})

clldf = pd.DataFrame({'longitude':crime_df.longitude,'latitude':crime_df.latitude})
clldf[['newLong','newLat']] = clldf.apply(convertCoords,axis=1)
crime_df['webLongitude']=clldf.newLong
crime_df['webLatitude']=clldf.newLat

# CONVERT PUPPY ZIP CODES TO LAT, LONG AND CONVERT TO WEB MERCATO
puppy_df = puppy_df[(puppy_df['zipcode'] < '28000')]

search = SearchEngine(simple_zipcode=True)
lat=[]
long=[]
for l in puppy_df.zipcode:
    zipcode = search.by_zipcode(l)
    lat.append(zipcode.lat)
    long.append(zipcode.lng)

puppy_df['latitude'] = lat
puppy_df['longitude'] = long
plldf = pd.DataFrame({'longitude':puppy_df.longitude,'latitude':puppy_df.latitude})
plldf[['newLong','newLat']] = plldf.apply(convertCoords,axis=1)
puppy_df['weblatitude'] = plldf.newLat
puppy_df['weblongitude'] = plldf.newLong

# MAP OF NYC
output_file("NYCmap.html")


# PLOT FIGURE 
p = figure(x_axis_type="mercator", y_axis_type="mercator")

p.add_tile(CARTODBPOSITRON)
p.circle(x=crime_df.webLongitude, y=crime_df.webLatitude, size=2, color="blue")
p.circle(x=puppy_df.weblongitude, y=puppy_df.weblatitude, size=2, color="red")

show(p)


script, div = components(p)