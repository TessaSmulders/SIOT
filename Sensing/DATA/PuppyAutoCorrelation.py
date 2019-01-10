import pandas as pd
import numpy as np
from sodapy import Socrata

import datetime as dt
 
from bokeh.plotting import *
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict, Counter
from bokeh.plotting import figure, show, output_file,curdoc

from bokeh.layouts import column


import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
from pylab import rcParams

from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_process import ArmaProcess
from statsmodels.tsa.arima_model import ARIMA


import matplotlib.gridspec as gridspec
from pandas.plotting import autocorrelation_plot, lag_plot



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
 

ts = inc["value"]
#plt.figure(figsize=(20, 10))
#ts.asfreq('M').plot()

acf = plot_acf(ts, lags=100,title="San Diego")
acf.set_figheight(4)
acf.set_figwidth(12)

plt.show()



selectedLagPoints = [1,3,6,9,12,24,36,48,60]
maxLagDays = 7

originalSignal = inc['value']

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

#ts =alb
#rcParams['figure.figsize'] = 11, 9
#decomposed = sm.tsa.seasonal_decompose(ts,freq=12) # The frequncy is annual
#figure = decomposed.plot()
#plt.show()