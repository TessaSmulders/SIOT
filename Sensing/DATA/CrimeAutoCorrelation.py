import pandas as pd
import numpy as np

import datetime
 
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict
from bokeh.plotting import figure, show, output_file

from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima_model import ARIMA
from pylab import rcParams
import matplotlib.pyplot as plt

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

## Get our "weeks" and "days"

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
cinc = cinc[cinc.date != '2013-01-01']

ts = cinc["value"]
plt.figure(figsize=(20, 10))
ts.asfreq('Y').plot()

acf = plot_acf(ts, lags=100,title="San Diego")
acf.set_figheight(4)
acf.set_figwidth(12)
plt.show()

selectedLagPoints = [1,3,6,9,12,24,36,48,60]
maxLagDays = 7

originalSignal = cinc['value']

# set grid spec of the subplots
plt.figure(figsize=(12,6))
gs = gridspec.GridSpec(2, len(selectedLagPoints))
axTopRow = plt.subplot(gs[0, :])
axBottomRow = []
for i in range(len(selectedLagPoints)):
    axBottomRow.append(plt.subplot(gs[1, i]))

# plot autocorr
allTimeLags = np.arange(1,maxLagDays*24)
autoCorr = [originalSignal.autocorr(lag=dt) for dt in allTimeLags]
axTopRow.plot(allTimeLags,autoCorr); 
axTopRow.set_title('Autocorrelation Plot of Puppies Being Born', fontsize=18);
axTopRow.set_xlabel('time lag [hours]'); axTopRow.set_ylabel('correlation coefficient')
selectedAutoCorr = [originalSignal.autocorr(lag=dt) for dt in selectedLagPoints]
axTopRow.scatter(x=selectedLagPoints, y=selectedAutoCorr, s=50, c='r')

# plot scatter plot of selected points
for i in range(len(selectedLagPoints)):
    lag_plot(originalSignal, lag=selectedLagPoints[i], s=0.5, alpha=0.7, ax=axBottomRow[i])    
    if i >= 1:
        axBottomRow[i].set_yticks([],[])
plt.tight_layout()



fig, ax = plt.subplots(nrows=4,ncols=1, figsize=(14,14))

timeLags = np.arange(1,25*24*30)
autoCorr = [originalSignal.autocorr(lag=dt) for dt in timeLags]
ax[0].plot(1.0/(24*30)*timeLags, autoCorr); ax[0].set_title('Autocorrelation Plot', fontsize=20);
ax[0].set_xlabel('time lag [months]'); ax[0].set_ylabel('correlation coeff', fontsize=12);

timeLags = np.arange(1,20*24*7)
autoCorr = [originalSignal.autocorr(lag=dt) for dt in timeLags]
ax[1].plot(1.0/(24*7)*timeLags, autoCorr);
ax[1].set_xlabel('time lag [weeks]'); ax[1].set_ylabel('correlation coeff', fontsize=12);

timeLags = np.arange(1,20*24)
autoCorr = [originalSignal.autocorr(lag=dt) for dt in timeLags]
ax[2].plot(1.0/24*timeLags, autoCorr);
ax[2].set_xlabel('time lag [days]'); ax[2].set_ylabel('correlation coeff', fontsize=12);

timeLags = np.arange(1,3*24)
autoCorr = [originalSignal.autocorr(lag=dt) for dt in timeLags]
ax[3].plot(timeLags, autoCorr);
ax[3].set_xlabel('time lag [hours]'); ax[3].set_ylabel('correlation coeff', fontsize=12);



alb = inc["value"]
alb.plot(figsize=(16,8))