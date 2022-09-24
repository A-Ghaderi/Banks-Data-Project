#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Import libraries ##
import pandas as pd
import numpy as np
import datetime
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

# Optional Plotly Method Imports
import cufflinks as cf
cf.go_offline()

## Read the data ##
df = pd.read_pickle('all_banks')
df.head()


# In[ ]:


## Creating a list of the ticker symbols (as strings) in alphabetical order ##
tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']

## Concatenating the bank dataframes together to a single data frame called bank_stocks ##
bank_stocks = pd.concat([df['BAC'], df['C'], df['GS'], df['JPM'], df['MS'], df['WFC']],axis=1,keys=tickers)
bank_stocks.columns.names = ['Bank Ticker','Stock Info']
bank_stocks.head()


# In[ ]:


## The max Close price for each bank's stock throughout the time period ##
bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()

## Creating a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock ##
returns = pd.DataFrame()
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
returns.head()


# In[ ]:


## A pairplot using seaborn of the returns dataframe ##
import seaborn as sns
sns.pairplot(returns[1:])

## On what dates each bank stock had the best and worst single day returns ##
returns.idxmin()
returns.idxmax()

## The standard deviation of the returns, which shows the riskiest over the entire time period ##
returns.std()
returns.ix['2015-01-01':'2015-12-31'].std()

## Distplot using seaborn of the 2015 returns for Morgan Stanley ##
sns.distplot(returns.ix['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=100)


# In[ ]:


## Showing Close price for each bank for the entire index of time ##

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()

bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()


# In[ ]:


## The rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008 ##
plt.figure(figsize=(12,6))
BAC['Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].ix['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()

## The correlation between the stocks Close Price ##
sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)

