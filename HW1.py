import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
from matplotlib.dates import date2num
import numpy as np
import herst #import loaded file herst.py
import datetime as dt

#region Select necessary data

#read csv, select dates
file = pd.read_csv('eurusd_h1.csv', sep=',')
mov_avg_window = 72

#need to merge date & time columns to get date-time value
file['date'] = pd.to_datetime(file['date'] +' '+ file['time']) #merge date&time
file = file[(file['date'] >= dt.datetime(2003,4,8)) & (file['date'] <= dt.datetime(2004,4,7))]
print(file)

#endregion

# region Plot it

file['date'] = date2num(file['date']) #convert time to float
file = file[['date', 'open','close','high','low']] #select columns & change order

quotes = file.values #convert to arrray
quotes = quotes.reshape(len(file), 5) #change matrix columns and rows

fig, ax = plt.subplots() #create new plot
fig.subplots_adjust(bottom=0.2)
mpf.candlestick_ochl(ax, quotes=quotes, width=0.02, alpha=1) #build candlestick graph
plt.show() #open graph

# endregion

# region Calculating returns

file['return_close'] = file['close'] / file['close'].shift() - 1 #calculate returns
file['MA_return'] = file['return_close'].rolling(window=mov_avg_window).mean() #moving avg of returns
file = file.dropna()

# endregion

#region Stat analisys

print('Средняя доходность = {:.4f}%'.format((file['return_close'].mean() * 100)))
print('Стандартное отклонение доходности = {:.4f}%'.format((file['return_close'].std() * 100)))
print('Медиана доходности = {:.4f}%'.format((file['return_close'].median() * 100)))

#endregion

#region Convert into arrays as I don't like working with pandas columns

returns = file['return_close'].values
MA_returns = file['MA_return'].values

herstes = [] #create array hor herst coef
for i in range(0, len(returns)): #file.index:
    try: #as the value error will occure
        h, c, data = herst.compute_Hc(returns[i-mov_avg_window:i], #calculate herst coef
                                      kind='change',
                                      simplified=False
                                      )
        herstes.append(h) #add it to array
    except ValueError:
        continue

#endregion

#region Momentum (buy if it grows, sell if it falls)

profits_momentum = []
Sum_Return = 1
for i in range(0, len(MA_returns)):
    if MA_returns[i] > 0:
        profits_momentum.append(1 + returns[i]) #if mean(r) > 0, add profit into profits array
    if MA_returns[i] < 0:
        profits_momentum.append(1 - returns[i]) #if mean(r) < 0, add profit into profits array with negative sign

for i in range(0, len(profits_momentum)):
    Sum_Return *= profits_momentum[i] #multiply all profits
print('Momentum strategy return = {:.4f}%'.format((Sum_Return - 1)*100))

#endregion

#region Reversion (vice versa)

profits_reversion = []
Sum_Return = 1
for i in range(0, len(MA_returns)):
    if MA_returns[i] < 0:
        profits_reversion.append(1 + returns[i])
    if MA_returns[i] > 0:
        profits_reversion.append(1 - returns[i])

for i in range(0, len(profits_reversion)):
    Sum_Return *= profits_reversion[i]
print('Mean reversion strategy return = {:.4f}%'.format((Sum_Return - 1)*100))

#endregion

#region Herst (use momentum or reversion based on herst coef)

profits_herst = []
Sum_Return = 1
for i in range(0, len(herstes)):
    if herstes[i] > 0.5:
        if MA_returns[i] > 0:
            profits_herst.append(1 + returns[i])
        if MA_returns[i] < 0:
            profits_herst.append(1 - returns[i])

    if herstes[i] < 0.5:
        if MA_returns[i] < 0:
            profits_herst.append(1 + returns[i])
        if MA_returns[i] > 0:
            profits_herst.append(1 - returns[i])

for i in range(0, len(profits_herst)):
    Sum_Return *= profits_herst[i]
print('Herst strategy return = {:.4f}%'.format((Sum_Return - 1)*100))

#endregion

#region Cumulative return graph

x = file['date'].values #create array of dates

#reshape them as they are rows, not columns
x = x.reshape(len(x), 1)
y_momentum = np.cumprod(np.array(profits_momentum))
y_reversion = np.cumprod(np.array(profits_reversion))
y_herst = np.cumprod(np.array(profits_herst))

#construct graphs
plt.plot(x, y_momentum, color='red', label='Momentum')
plt.plot(x, y_reversion, color='green', label='Mean reversion')
x_herst = x[mov_avg_window:]
plt.plot(x_herst, y_herst, color='black', label='Herst')
plt.grid() #add grid
plt.legend() #add legend
plt.show()

#endregion