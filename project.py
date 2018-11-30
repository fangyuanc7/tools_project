!pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
!pip install tabulate
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import fix_yahoo_finance as yf
from tabulate import tabulate
import seaborn
import scipy.stats
from scipy.stats import norm
import math
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def inputime():
    while True:
        try:
            ticker = input("What equity would you like to analyze? ")
            url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
            response = requests.get(url, verify=False)
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
    return start_date, end_date, ticker

start_, end_, ticker = inputime()

while not (datetime.datetime(1970,1,1) < start_ <= datetime.datetime.now()) and (datetime.datetime(1970,1,1) < end_ <= datetime.datetime.now()):
    print("Your input time is out of our data bounds, please input again")
    start_, end_, ticker = inputime()

print("Analyzing " + str(ticker) + " between the dates of " + str(start_) + " and " + str(end_) + ": ")
df = web.DataReader([ticker], 'yahoo', start_, end_)
df['Date'] = df.index.values
print(df.head(10))

def plot_historical_prices(df):
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Adj Close'],label = 'Price')
    long_rolling =  df['Adj Close'].rolling(window=15).mean()
    long_rolling_std = df['Adj Close'].rolling(window=15).std()    
    upper_band = long_rolling + (long_rolling_std*1.5)
    lower_band = long_rolling - (long_rolling_std*1.5)
    ema_short = df['Adj Close'].ewm(span=20, adjust=False).mean()
    plt.title(str(ticker) + ' Price from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Stock Value')
    plt.xlabel('Date')
    plt.plot(df['Date'], ema_short, label = 'Span 20-days EMA')
    plt.plot(df['Date'], long_rolling, label = 'Simple Moving Avg')    
    plt.plot(df['Date'], upper_band, label = 'Upper Band')
    plt.plot(df['Date'], lower_band, label = 'Lower Band') 
    plt.legend(loc = 'best')
    plt.show()

def plot_log_returns(df):
    df_copy = df.copy(deep=True)
    df_copy = df_copy.iloc[1:]
    df_copy['Log Returns'] = (np.log(df_copy['Adj Close']) - np.log(df_copy['Adj Close'].shift(1)))
    #df_copy['pct change'] = df_copy['Adj Close'].pct_change()
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.ylim(-.1, .1) #Edit this to be customized later
    plt.xlim(start_,end_)
    plt.plot(df_copy['Date'], df_copy['Log Returns'])
    plt.title(str(ticker) + ' Log returns from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Log Returns')
    plt.xlabel('Date')
    plt.show()

def plot_historical_volume(df):
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Volume'])
    plt.title(str(ticker) + ' Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.show()
    
def plot_daily_volatility(df):
    df_copy = df.copy(deep = True)
    df_copy['Daily Volatility'] =  (df_copy['High'] - df_copy['Low'])/(df_copy['High'] + df_copy['Low'])
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.ylim(-.1, .1) #Edit this to be customized later
    plt.xlim(start_, end_)
    plt.plot(df_copy['Date'], df_copy['Daily Volatility'])
    plt.title(str(ticker) + ' Daily Volatility from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Daily Volatility')
    plt.xlabel('Date')
    plt.show()
    
def plot_Value_at_Risk(df):
    pd.options.mode.chained_assignment = None
    
    df = df[['Close']]
    df['Returns'] = df.Close.pct_change()
    mean = np.mean(df['Returns'])
    std = np.std(df['Returns'])
    
    df['Returns'].hist(bins = 40, histtype = 'bar', alpha = 1)
    x = np.linspace(mean - 3*std, mean + 3*std, 100)
    plt.rcParams['figure.figsize'] = [10, 5]
    plt.plot(x, scipy.stats.norm.pdf(x, mean, std), "r")
    plt.title(str(ticker) + ' Value at Risk (VaR) from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Frequency')
    plt.xlabel('Returns')
    plt.show()
    
    VaR_90perc = norm.ppf(.1, mean, std)
    VaR_95perc = norm.ppf(.05, mean, std)
    VaR_99perc = norm.ppf(.01, mean, std)
    
    print(tabulate([['90%', VaR_90perc], ['95%', VaR_95perc], ['99%', VaR_99perc]], 
                   headers = ['Confidence Level', 'Value at Risk']))

def plot_Point_and_Figure(df):
    BOX = 2
    #START = 300
    #print(df['Adj Close'].iloc[1])
    START = df['Adj Close'].iloc[0]
    df_copy = df.copy(deep = True)
    #df_copy = df_copy.iloc[1:]
    
    df_copy['changes'] = (df_copy['Adj Close'] - df_copy['Adj Close'].shift(1))
    df_copy = df_copy.drop(df.index[0])
    #print(df_copy['changes'])
    #for chg in df_copy['changes']:
    #    print(chg)
    #print(changes)
    
    fig = plt.figure(figsize=(5, 10))
    ax = fig.add_axes([.15, .15, .7, .7])

    def sign(val):
        if val == 0:
            return 0
        else:
            return (val / abs(val))

    pointChanges = []
   
    for chg in df_copy['changes']:
#        print(sign(float(chg)))
#        print(math.floor(abs(float(chg))))
#         print(type(chg))
#         print(float(chg))
#         print(sign(chg))
#         print(abs(chg))
        pointChanges += [sign(float(chg))] * math.floor(abs(float(chg)))
    
#PLOTTING HERE
# plot_historical_prices(df)
# plot_log_returns(df)
# plot_historical_volume(df)
# plot_daily_volatility(df)
# plot_Value_at_Risk(df)
# plot_Point_and_Figure(df)

from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.pyplot import subplots, draw
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt

def plot_candlestick(df):
    from matplotlib import dates as mdates
    from matplotlib import ticker as mticker
    from mpl_finance import candlestick_ohlc
    import datetime as dt
    df_copy = df.copy(deep=True)
    data = df_copy
    df_copy['Date'] = mdates.date2num(df_copy['Date'].astype(dt.date))
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))
    plt.title(str(ticker) + ' Candlestick Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Candlestick Volume')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(6))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    p = candlestick_ohlc(ax1, df_copy.values, width=0.2)
    dataAr = [tuple(x) for x in df_copy[['Date', 'Open', 'Close', 'High', 'Low']].to_records(index = False)]
    fig = plt.figure()
    ax1 = plt.subplot(1,1,1)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    candlestick_ohlc(ax1, dataAr)
    plt.title(str(ticker) + ' Candlestick Movement from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Price')
    plt.xlabel('Date')
    plt.show()

# plot_candlestick(df)

#create a dropdown menu for the graphs display based on user input

from tkinter import *
OPTIONS = [
"Please Choose One Type of Graph",
"Historical Prices",
"Log Returns",
"Historical Volume",
"Daily Volatility",
"Value at Risk (VaR)",
"Candlestick",
"Max Drawdown Plot",
"Momentum Oscillators"
] 

master = Tk()
master.title("Select the type of data visualization")

# Add a grid
mainframe = Frame(master)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 200)

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

def ok():
    print ("Graph You Picked Is: " + variable.get())
    
button = Button(master, text="Visualize", command=ok)
button.pack()

mainloop()

graph= variable.get()
if graph == OPTIONS[1]:
    plot_historical_prices(df)
elif graph == OPTIONS[2]:
    plot_log_returns(df)
elif graph == OPTIONS[3]:
    plot_historical_volume(df)
elif graph == OPTIONS[4]:
    plot_daily_volatility(df)
elif graph == OPTIONS[5]:
    plot_Value_at_Risk(df)
elif graph == OPTIONS[6]:
    plot_candlestick(df)
