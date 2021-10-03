###Data Preprocessing

import pandas as pd

restaurant_visitors = \
    pd.read_csv('restaurants_visitors.csv'
                , keep_default_na=False, na_values=[''])
date_info = \
    pd.read_csv('date_info.csv'
                , keep_default_na=False, na_values=[''])
store_info = \
    pd.read_csv('store_info.csv'
                , keep_default_na=False, na_values=[''])

# making the property changes

date_info1 = date_info.dropna()
restaurant_visitors['visit_datetime'] = \
    pd.to_datetime(restaurant_visitors['visit_datetime'],
                   format='%d/%m/%Y %H:%M').dt.to_period('D')
rest_tot = restaurant_visitors[['id', 'visit_datetime',
                                'reserve_visitors']]

date_info1['calendar_date'] = date_info1['calendar_date'].astype(str)
rest_tot['visit_datetime'] = rest_tot['visit_datetime'].astype(str)
result = pd.merge(left=date_info1, right=rest_tot,
                  left_on='calendar_date', right_on='visit_datetime',
                  how='inner')
all_result = pd.merge(left=result, right=store_info, left_on='id',
                      right_on='store_id', how='inner')
columns_to_drop = ['calendar_date', 'store_id', 'area_name', 'latitude'
    , 'longitude']
all_result = all_result.drop(columns_to_drop, axis=1)
all_result.to_csv('union_all.csv'
                  )

###Time Series

import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')
import pandas as pd
import statsmodels.api as sm
import matplotlib

matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'

df = pd.read_csv("union_all.csv")

rest = df.sort_values('visit_datetime')
rest.isnull().sum()
rest = furniture.groupby('visit_datetime')['reserve_visitors'].sum().reset_index()
rest = rest.set_index('visit_datetime')
rest.index
y = rest['reserve_visitors']
y.plot(figsize=(15, 6))
plt.show()

from pylab import rcParams

rcParams['figure.figsize'] = 18, 8
decomposition = sm.tsa.seasonal_decompose(y, model='additive', freq=3)

fig = decomposition.plot()
plt.show()

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

####Getting parameter selection restaurant’s visitors ARIMA TSM.

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

### Test and results
mod = sm.tsa.statespace.SARIMAX(y,
                                order=(1, 1, 1),
                                seasonal_order=(1, 1, 0, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit()
print(results.summary().tables[1])

pred = results.get_prediction(dynamic=False)
pred_ci = pred.conf_int()
print(pred_ci)
ax = y['2016':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 1],
                pred_ci.iloc[:, 0], color='k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('Visitors arrived')
plt.legend()
plt.show()

pred = results.get_prediction(dynamic=False)
pred_ci = pred.conf_int()
print(pred_ci)
ax = y['2016':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7, figsize=(14, 7))
ax.set_xlabel('Date')
ax.set_ylabel('Visitors arrived')
plt.legend()
plt.show()
