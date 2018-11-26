import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import fix_yahoo_finance as yf
#import googlefinance.client

def inputime():
   # ticker = input("What equity would you like to analyse? ")
    while True:
    try:
        ticker = input("What equity would you like to analyse? ")
        url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
        response = requests.get(url, verify=False)
        sleep(4)
        other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
        summary_json_response = requests.get(other_details_json_link)
        if not summary_json_response.status_code == 200:
            raise ValueError
        else:
            break
    except ValueError:
        print('\033[1m' + 'Please Input A Valid Ticker For Analysis. Please Try Again.')
        
    start = input("When would you like to begin analyzing? Please enter date in format YYYY/MM/DD: ")
    end = input("When would you like to end analyzing? Please enter date in format YYYY/MM/DD: ")

    #Can add allowance of multiple ticker input here later

    start_date = start.split('/')
    start_year = int(start_date[0])
    start_month = int(start_date[1])
    start_day = int(start_date[2])
    start_date = datetime.datetime(start_year, start_month, start_day)

    end_date = end.split('/')
    end_year = int(end_date[0])
    end_month = int(end_date[1])
    end_day = int(end_date[2])
    end_date = datetime.datetime(end_year, end_month, end_day)

    return start_date,end_date,ticker

start_,end_,ticker = inputime()

while not (datetime.datetime(1970,1,1) < start_ <= datetime.datetime.now()) and (datetime.datetime(1970,1,1) < end_ <= datetime.datetime.now()):
    print("Your input time is out of our data bounds, please input again")
    start_,end_,ticker = inputime()
#Add try/except ValueError if input ticker is not available in yahoo finance database

#Add try/except ValueError check here to make sure the input start/end year is within our data bounds 
#i.e. check 1950?<=Year<=2018); 1<=month<=12; 1<=day<=28/30/31

#print(df.head(10))

print("Analyzing " +str(ticker) + " between the dates of " + str(start_) + " and " +str(end_) + ": ")
df = web.DataReader([ticker], 'yahoo', start_, end_)
df['Date'] = df.index.values
print(df.head(10))

#Visualize the stock's historical movement / volume
#Compare to other stocks?
def plot_historical_prices(df):
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Adj Close'])
    plt.title(str(ticker) + ' Price from ' + str(start_date)[0:11] + 'to ' + str(end_date)[0:11])
    plt.ylabel('Stock Value')
    plt.xlabel('Date')
    plt.show()

plot_historical_prices(df)

def plot_log_returns(df):
    df_copy = df.copy(deep=True)
    df_copy = df_copy.iloc[1:]
    df_copy['Log Returns'] = (np.log(df_copy['Adj Close']) - np.log(df_copy['Adj Close'].shift(1)))
    #df_copy['pct change'] = df_copy['Adj Close'].pct_change()
    #print(df_copy)
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.ylim(-.1, .1) #Edit this to be customized later
    plt.xlim(start_date,end_date)    
    plt.plot(df_copy['Date'], df_copy['Log Returns'])
    plt.title(str(ticker) + ' Log returns from ' + str(start_date)[0:11] + 'to ' + str(end_date)[0:11])
    plt.ylabel('Log Returns')
    plt.xlabel('Date')
    plt.show()
    
    #print(df['Adj Close']['AAPL'][1:])
    #print(df['Adj Close']['AAPL'][1:]-df['Adj Close']['AAPL'][4:])
    
    #print(df['Adj Close'][1:]-df['Adj Close'][2:])    
    
    #df['Daily Returns'] = df['Adj Close']-df['Adj Close']
    #print(df)
    #df['Daily Returns'] = np.diff(df['Adj Close'])/df['Adj Close']
    #df
#     plt.plot(df['Date'], df['Adj Close'])
#     plt.title(str(ticker) + ' Price from ' + str(start_date)[0:11] + 'to ' + str(end_date)[0:11])
#     plt.ylabel('Stock Value')
#     plt.xlabel('Date')
#     plt.show()

plot_log_returns(df)


def plot_historical_volume(df):
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Volume'])
    plt.title(str(ticker) + ' Volume from ' + str(start_date)[0:11] + 'to ' + str(end_date)[0:11])
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.show()

plot_historical_volume(df)
