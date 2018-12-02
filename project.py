## pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
# !pip install tabulate
# !pip install numpy
# !pip install pandas
# !pip install requests
# !pip install bs4
# !pip install datetime
# !pip install matplotlib.pylot
# !pip install pandas_datareader.data
# !pip install fix_yahoo_finance
# !pip install seaborn
# !pip install scipy.stats
# !pip install math
# !pip install urllib3
# !pip install tkinter

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
from tkinter import *

def user_input():
    '''
    Main function where user inputs stock ticker and time periods for analysis and data visualization. 
    '''
    
    while True:
        try:
            ticker = input("What equity would you like to analyze? Please enter the ticker name (Case Insensitive): ")
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

    while True:
        try:
            start = input("When would you like to begin analyzing? Please enter date in format YYYY/MM/DD: ")
            end = input("When would you like to end analyzing? Please enter date in format YYYY/MM/DD: ")
                        
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
            
            if start_date >= end_date:
                print('\033[1m' + "Your start date must be earlier than end date, please input again")
            elif (datetime.datetime(1970,1,1) < start_date <= datetime.datetime.now()) and (datetime.datetime(1970,1,1) < end_date <= datetime.datetime.now()):
                break
            else:
                print('\033[1m' + "Your input time is out of our data bounds, please input again")  
        except:
            print('\033[1m' + "Your input time is illegal, please input again")
    
    return start_date, end_date, ticker

start_, end_, ticker = user_input()

print("Analyzing " + str(ticker) + " between the dates of " + str(start_)[0:10] + " and " + str(end_)[0:10] + ": ")
df = web.DataReader([ticker], 'yahoo', start_, end_)
df['Date'] = df.index.values
#print(df.head(10))

def plot_historical_prices(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a plot with historical prices, 
    as well as a moving average curve and Bollinger Bands attached.
    '''
    
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Adj Close'], label = 'Price')

    long_rolling =  df['Adj Close'].rolling(window = 15).mean()
    long_rolling_std = df['Adj Close'].rolling(window = 15).std()    
    upper_band = long_rolling + (long_rolling_std * 2)
    lower_band = long_rolling - (long_rolling_std * 2)
    
    plt.title(str(ticker) + ' Price from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Stock Value')
    plt.xlabel('Date')
    plt.plot(df['Date'], long_rolling, label = 'Simple Moving Avg')    
    plt.plot(df['Date'], upper_band, label = 'Upper Band')
    plt.plot(df['Date'], lower_band, label = 'Lower Band') 
    plt.legend(loc = 'best')
    plt.show()
    
    description ='A moving average is a widely used indicator in technical analysis that helps smooth out price action by filtering'
    description +=' out the “noise” from random price fluctuations. '
    description += 'It is a trend-following, or lagging, indicator because it is based on past prices.'
    
    print(description)
    
    d2 = 'A Bollinger Band is a set of lines plotted two standard deviations (positively and negatively) away from a simple moving'
    d2 += "average of the security's price. It is normally plotted two standard deviations away from a simple moving average"
    
    print(d2)
    
def plot_log_returns(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a plot with log returns.
    '''

    df_copy = df.copy(deep = True)
    df_copy = df_copy.iloc[1:]
    df_copy['Log Returns'] = (np.log(df_copy['Adj Close']) - np.log(df_copy['Adj Close'].shift(1)))
    #df_copy['pct change'] = df_copy['Adj Close'].pct_change()
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.ylim(-.2, .2) 
    plt.xlim(start_, end_)
    plt.plot(df_copy['Date'], df_copy['Log Returns'])
    plt.title(str(ticker) + ' Log returns from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Log Returns')
    plt.xlabel('Date')
    plt.show()
    
    description = "Rather than calculating the normal differences and returns, we present a lognormal returns "
    description += "graph. The advantages of using log returns compared to raw differences in prices are that "
    description += "arithmetic returns would have a positive bias (stock prices cannot fall below zero); this "
    description += "bias is eliminated through taking the log as that normalizes the returns. This is furthermore "
    description += "important because stocks grow at a compounded rate based on the prior day's value."
    
    print(description)
    
def plot_cdf(df):
    '''
    Takes in dataframe with close prices and returns a Cumulative Distribution Function of returns.
    '''
    
    ##Change to 1
    plt.rcParams['figure.figsize'] = [20, 15]
    start_date_price = df.iloc[0, 5]
    cum_return = (df['Adj Close']-start_date_price)/start_date_price
    plt.plot(df['Date'],cum_return)
    plt.title(' Cumulative Return of ' + str(ticker) + ' from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Cumulative Return')
    plt.xlabel('Date')
    plt.show()
    
    description = "CDF DESCRIPTION HERE"
    
    print(description)
    
def plot_historical_volume(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a graph with the historical trading volume.
    '''
    
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Volume'])
    plt.title(str(ticker) + ' Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Volume')
    plt.xlabel('Date')
    plt.show()
    
    description = "The historical trading volume shows how often the stock has been traded in the past and can be " 
    description += "used in conjunction with the other graphs to examine the market sentiment and stock liquidity."
    
    print(description)
    
def plot_daily_volatility(df):
    '''
    Takes in dataframe with interday high and low prices and returns a plot with daily volatility.
    '''
    
    df_copy = df.copy(deep = True)
    df_copy['Daily Volatility'] =  (df_copy['High'] - df_copy['Low'])/(df_copy['High'] + df_copy['Low'])
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.ylim(-.2, .2)
    plt.xlim(start_, end_)
    plt.plot(df_copy['Date'], df_copy['Daily Volatility'])
    plt.title(str(ticker) + ' Daily Volatility from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Daily Volatility')
    plt.xlabel('Date')
    plt.show()
    
    description = 'Daily changes in a price of a good or service based on imbalances between the supply and demand.'
    description += 'Current market conditions can greatly impact price of goods and high degrees of volatility can cause '
    description += 'panic and drive prices up when there is fear of too few sellers compared to buyers.'
    
    print(description)
    
def plot_Value_at_Risk(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a Value at Risk curve.
    '''
    
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

    description = "\nThis Value at Risk curve shows the user the potential risk and volatility of the input stock. "
    description += "VaR helps answer the question of 'Within a specific confidence level, how much money could I lose "
    description += "in this investment?' The table above shows that, within a 90, 95, and 99 percentile confidence " 
    description += "level, the user by investing in the input stock could expect to, in a worst case scenario, lose "
    description += "up to the respective percentage level."

    print(description)
    
def plot_Point_and_Figure(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a Point and Figure chart.
    '''
    
    BOX = 2
    START = df['Adj Close'].iloc[0]
    df_copy = df.copy(deep = True)    
    df_copy['changes'] = (df_copy['Adj Close'] - df_copy['Adj Close'].shift(1))
    df_copy = df_copy.drop(df.index[0])
    fig = plt.figure(figsize = (5, 10))
    ax = fig.add_axes([1, 1, 2, 2])

    def sign(val):
        if val == 0:
            return 0
        else:
            return (val / abs(val))

    change_points = []
    for change in df_copy['changes']:
        change_points += [sign(float(change))] * math.floor(abs(float(change)))
        symbol = {-1:'o',
                   0:'None',
                   1:'x'}

    change_start = START
    for x_change, change in enumerate(df_copy['changes']):
        x = [x_change + 1] * math.floor(abs(change))
        y = [change_start + i * BOX * sign(float(change)) for i in range(math.floor(abs(change)))] 
        change_start += BOX * sign(float(change)) * (math.floor(abs(change))-2)
        ax.scatter(x, y,
                   marker = symbol[sign(float(change))],
                   c = 'blue', 
                   s = 100)   

    ax.set_xlim(0, len(df_copy['changes']) + 1)
    plt.title(str(ticker) + ' Point and Figure Chart from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Price')
    plt.xlabel('Frequency')
    #ax = fig.gca()
    #print(df_copy['Low'].min()[0])
    #ax.set_xticks(np.arange(0, len(df_copy['Low']), 2))
    #ax.set_yticks(np.arange(df_copy['Low'].min()[0]-10, df_copy['High'].max()[0]+10, 2))
    #plt.grid()
    plt.show()  
    
    description = "Point and Figure charts allow the user to identify significant changes in the price. Instead of the "
    description += "horizontal axis representing time, as it does in many of the other plots, it instead represents "
    description += "changes in direction. Any up movements of a significant amount are charted as an 'X', and any "
    description += "down movements of a significant amount are charted as an 'O'. There are several advantages to "
    description += "using a P&F Chart, such as filtering out insignificant price movements and noise, as well as " 
    description += "allowing the user to distinguish support and resistance levels for the stock."
        
    print(description)

def plot_Relative_Strength_Index(df):
    '''
    Takes in dataframe with close prices and returns a Relative Strength Index with two-week moving averages.
    '''
    
    differences = df['Adj Close'].diff()
    window_length = 14
    
    days_up = differences.copy()
    days_up[differences <= 0] = 0.0
    days_down = abs(differences.copy())
    days_down[differences > 0] = 0.0
    
    rolling_up = days_up.rolling(window_length).mean()
    rolling_down = days_down.rolling(window_length).mean()
    
    RSI = 100 - (100/(1+(rolling_up / rolling_down)))
    
    plt.figure()
    RSI.plot()
    plt.show()
    
    description = "The Relative Strength Index (RSI) is a momentum indicator that utilizes the magnitude of "
    description += "recent price movements to evaluate whether the asset is overbought or oversold. A RSI value "
    description += "above 70 is generally correlated with an overbought security, indicating potential downtrends "
    description += "in the future. Similarly, an RSI below 30 is generally correlated with an oversold security, "
    description += "indicating a potential uptick soon. RSI can be utilized with the other analysis chart tools "
    description += "for the user to gauge the overall market sentiment toward the security. Rolling window "
    description += "length used is typically 2 weeks, but this is user changeable."
    
    print(description)

def plot_candlestick(df):
    '''
    Takes in dataframe with Date, Open, Close, High, Low values and returns candlestick technical charts.
    '''
    
    from datetime import datetime, timedelta
    import matplotlib.dates as mdates
    from matplotlib.pyplot import subplots, draw
    from mpl_finance import candlestick_ohlc
    import matplotlib.pyplot as plt
    from matplotlib import dates as mdates
    from matplotlib import ticker as mticker
    from mpl_finance import candlestick_ohlc
    import datetime as dt
    df_copy = df.copy(deep = True)
    data = df_copy
    df_copy['Date'] = mdates.date2num(df_copy['Date'].astype(dt.date))
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1), (0,0))
    plt.title(str(ticker) + ' Candlestick Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Candlestick Volume')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(6))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) #date axis not formatted
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
    
    description = 'A candlestick is a type of price chart that displays the high, low, open and closing prices of a security'
    description += ' for a specific period. The wide part of the candlestick is called the "real body" '
    description += 'and tells investors whether the closing price was higher or lower than the opening price '
    description += 'with red if the stock closed lower, orange if the stock closed higher.'
    
    print(description)

def plot_max_drawdown(df):
    '''
    Takes in dataframe with high and low stock price, and returns a max daily drawdown plot with rolling window of 7.
    '''
    
    df_copy = df.copy(deep = True)
    Roll_Max = df_copy['Adj Close'].rolling(window=7).max()
    Daily_Drawdown = df_copy['Adj Close']/Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(window=7).min()
    plt.rcParams['figure.figsize'] = [15, 10]
    plt.ylim(-1, 0.1)
    plt.xlim(start_, end_)
    plt.plot(df_copy['Date'], Max_Daily_Drawdown)
    plt.title(str(ticker) + ' Max_Daily_Drawdown from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Max_Daily_Drawdown')
    plt.xlabel('Date')
    plt.show()
    
    description = "A maximum drawdown (MDD) is the maximum loss from a peak to a trough of a portfolio, "
    description += "before a new peak is attained. \nMaximum Drawdown (MDD) is an indicator of downside risk over a specified time period. "
    description += "\nMDD = (Trough Value – Peak Value) ÷ Peak Value"
    description += "\nIn this graph, it shows a rolling window of 7 days of daily maximum drawdown, given the time period provided by user."
    
    print(description)

#create a dropdown menu for the graphs display based on user selection
OPTIONS = [
        "Please Choose One Type of Graph",
        "Historical Prices",
        "Log Returns",
        "Cumulative Distribution Function",
        "Historical Volume",
        "Daily Volatility",
        "Value at Risk (VaR)",
        "Candlestick",
        "Point and Figure",
        "Max Drawdown Plot",
        "Relative Strength Index"
        ] 

master = Tk()
master.title("Select the type of data visualization")

# Add a grid
mainframe = Frame(master)
mainframe.grid(column = 0, row = 0, sticky = (N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 200)

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

def confirm():
    print ("\n Graph You Picked Is: " + variable.get())
#     master.quit()
    
button = Button(master, text = "Visualize", command = confirm)
button.pack()

mainloop()

graph = variable.get()

def draw_graph():
    if graph == OPTIONS[1]:
        plot_historical_prices(df)
    elif graph == OPTIONS[2]:
        plot_log_returns(df)
    elif graph == OPTIONS[3]:
        plot_cdf(df)
    elif graph == OPTIONS[4]:
        plot_historical_volume(df)
    elif graph == OPTIONS[5]:
        plot_daily_volatility(df)
    elif graph == OPTIONS[6]:
        plot_Value_at_Risk(df)
    elif graph == OPTIONS[7]:
        plot_candlestick(df)
    elif graph == OPTIONS[8]:
        plot_Point_and_Figure(df)
    elif graph == OPTIONS[9]:
        plot_max_drawdown(df)
    elif graph == OPTIONS[10]:
        plot_Relative_Strength_Index(df)
        
draw_graph()
