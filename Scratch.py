import pandas as pd
import numpy as np
# import math
# import sklearn.linear_model as skl
import datetime as dt
# import re, requests
# from bs4 import BeautifulSoup
# import time
# import re
# from sklearn.model_selection import cross_val_score
# from sklearn.tree import DecisionTree Classifier
# from sklearn.metrics import confusion_matrix
# from sklearn import tree
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import scipy

#region pandas print width

desired_width=150#len(file.columns)
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',10)

#endregion
#
# # region creating pvt
#
# df = pd.read_csv('old_AkBars.csv')
#
# print(df)

import pandas_datareader.data as web
startDate = '2016-1-1'
endDate = dt.datetime.today()
ticker1 = '0486.HK'
ticker2 = 'RUAL.ME'
currency = 'HKDRUX=X'
mgWeb = web.DataReader(ticker1,'yahoo',startDate,endDate)
mgWeb2 = web.DataReader(ticker2,'yahoo',startDate,endDate)
mgWeb_currency = web.DataReader(currency,'yahoo',startDate,endDate)

mgWeb = pd.merge(mgWeb, mgWeb_currency, how = 'left', left_index=True, right_index=True, suffixes=['', '_currency'])
mgWeb = mgWeb.fillna(method='backfill')
mgWeb['Close_RUB'] = mgWeb['Close'] * mgWeb['Close_currency']

print(mgWeb)
print(mgWeb2)

plt.plot(mgWeb.index, mgWeb['Close_RUB'], label = ticker1)
plt.plot(mgWeb2.index, mgWeb2['Close'], label = ticker2)
plt.legend()
plt.show()