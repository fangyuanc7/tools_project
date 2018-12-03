# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
# pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
# !pip install numpy
# !pip install pandas
# !pip install requests
# !pip install datetime
# !pip install matplotlib.pylot
# !pip install pandas_datareader.data
# !pip install fix_yahoo_finance
# !pip install tabulate
# !pip install seaborn
# !pip install scipy.stats
# !pip install math
# !pip install urllib3
# !pip install ipywidgets

import numpy as np
import pandas as pd
import requests
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker as mticker
from matplotlib.pyplot import subplots, draw
from mpl_finance import candlestick_ohlc
import pandas_datareader.data as web
import fix_yahoo_finance as yf
from tabulate import tabulate
import seaborn
import scipy.stats
from scipy.stats import norm
import math
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from ipywidgets import widgets
from IPython.display import display

def user_input():
    '''
    Main function where user inputs stock ticker and time periods for analysis and data visualization. 
    '''
    
    ticker_list = []
    while True:
        while True:
            try:
                example = """
                        Here are some popular ticker names:
                        Apple: AAPL,
                        Amazon: AMZN,
                        Netflix: NFLX,
                        Alphabet Inc.: GOOG,
                        Bank of America Corporation: BAC
                        For more, click: https://finance.yahoo.com/trending-tickers
                         """
                print(example)
                ticker = input("What equity would you like to analyze? Please enter the ticker name (Case Insensitive): ")
                if ticker in ticker_list:
                    raise IOError
                url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker,ticker)
            
                response = requests.get(url, verify=False)
                other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
                summary_json_response = requests.get(other_details_json_link)
                if not summary_json_response.status_code == 200:
                    raise ValueError
                else:
                    ticker_list.append(ticker)
                    break
            except IOError:
                print('\033[1m' + 'Please input a ticker different from previous tickers')
            except ValueError:
                print('\033[1m' + 'Please Input A Valid Equity Ticker For Analysis. Please Try Again.') 
        while True:
            input_again = input("Do you want to analyze another equity? Please enter YES or NO(Case Insensitive): ")
            if input_again in ['YES','NO','yes','no']:
                break
            else:
                print('\033[1m' + 'Please enter YES or NO(Case Insensitive): ')
        if input_again == 'NO' or input_again == 'no': 
            break
    
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
    return start_date, end_date, ticker_list

start_, end_, tickers = user_input()
    
tickers_df_list = []   
for ticker in tickers:
    ticker_name = str(ticker).upper()
    print("Analyzing " + ticker_name + " between the dates of " + str(start_)[0:10] + " and " + str(end_)[0:10] + ": ")
    df = web.DataReader([ticker], 'yahoo', start_, end_)
    df['Date'] = df.index.values
    tickers_df_list.append(df)
    #print(df.head(10))

def plot_historical_prices(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a plot with historical prices, 
    as well as a moving average curve and Bollinger Bands attached.
   '''
  
    plt.rcParams['figure.figsize'] = [20, 15]
    plt.plot(df['Date'], df['Adj Close'], label = 'Price', linewidth=4)

    long_rolling =  df['Adj Close'].rolling(window = 15).mean()
    long_rolling_std = df['Adj Close'].rolling(window = 15).std() 
    upper_band = long_rolling + (long_rolling_std * 1.5)
    lower_band = long_rolling - (long_rolling_std * 1.5)

    ticker_name = str(ticker).upper()
    plt.title(ticker_name + ' Price from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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

    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        df_copy = df_copy.iloc[1:]
        df_copy['Log Returns'] = (np.log(df_copy['Adj Close']) - np.log(df_copy['Adj Close'].shift(1)))
        #df_copy['pct change'] = df_copy['Adj Close'].pct_change()
        plt.rcParams['figure.figsize'] = [20, 15]
        plt.ylim(-.2, .2) 
        plt.xlim(start_, end_)
        plt.plot(df_copy['Date'], df_copy['Log Returns'], label = tickers[i])
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Log returns from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Log returns from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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

    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        plt.rcParams['figure.figsize'] = [20, 15]
        start_date_price = df_copy.iloc[0, 5]
        cum_return = (df_copy['Adj Close']-start_date_price)/start_date_price
        plt.plot(df_copy['Date'],cum_return)
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Cumulative Return of '+ str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Cumulative Return of ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Cumulative Return')
    plt.xlabel('Date')
    plt.show()
    
    description = "A cumulative return is the aggregate amount an investment has gained or lost over time, "
    description += " independent of the period of time involved."
    print(description)
 
    
def plot_historical_volume(df):
    '''
    Takes in dataframe with time-series stock closing prices, and returns a graph with the historical trading volume.
    '''
    
    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        plt.rcParams['figure.figsize'] = [20, 15]
        plt.plot(df_copy['Date'], df_copy['Volume'], label = tickers[i] )
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Volume from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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
    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        df_copy['Daily Volatility'] =  (df_copy['High'] - df_copy['Low'])/(df_copy['High'] + df_copy['Low'])
        plt.rcParams['figure.figsize'] = [20, 15]
        plt.ylim(-.2, .2)
        plt.xlim(start_, end_)
        plt.plot(df_copy['Date'], df_copy['Daily Volatility'], label = tickers[i])
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Daily Volatility from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Daily Volatility from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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
    
    header = ['Confidence Level']
    perc90 = ['90%']
    perc95 = ['95%']
    perc99 = ['99%']
    
    pd.options.mode.chained_assignment = None
    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        df_copy = df_copy[['Close']]
        df_copy['Returns'] = df_copy.Close.pct_change()
        mean = np.mean(df_copy['Returns'])
        std = np.std(df_copy['Returns'])

        df_copy['Returns'].hist(bins = 40, histtype = 'bar', alpha = 1)
        x = np.linspace(mean - 3*std, mean + 3*std, 100)
        plt.rcParams['figure.figsize'] = [10, 15]
        plt.plot(x, scipy.stats.norm.pdf(x, mean, std), "r")
        
        ticker_name = 'Value at Risk of ' + str(tickers[i]).upper()
        header.append(ticker_name)
        
        VaR_90perc = norm.ppf(.1, mean, std)
        VaR_95perc = norm.ppf(.05, mean, std)
        VaR_99perc = norm.ppf(.01, mean, std)
        perc90.append(VaR_90perc)
        perc95.append(VaR_95perc)
        perc99.append(VaR_99perc)
        
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Value at Risk (VaR) from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Value at Risk (VaR) from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Frequency')
    plt.xlabel('Returns')
    plt.show()
    
    print(tabulate([perc90,perc95,perc99], headers = header))

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
    plt.title(str(ticker).upper() + ' Point and Figure Chart from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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
    
    window_length = 14
    
    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        differences = df_copy['Adj Close'].diff()
        days_up = differences.copy()
        days_up[differences <= 0] = 0.0
        days_down = abs(differences.copy())
        days_down[differences > 0] = 0.0

        rolling_up = days_up.rolling(window_length).mean()
        rolling_down = days_down.rolling(window_length).mean()

        RSI = 100 - (100/(1+(rolling_up / rolling_down)))
        plt.plot(df_copy['Date'],RSI,label = tickers[i])
    if len(tickers) == 1: 
        plt.title(str(ticker).upper() + ' Value at Risk (VaR) from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) >= 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Value at Risk (VaR) from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.figure()
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
    df_copy = df.copy(deep = True)
    df_copy['Date'] = mdates.date2num(df_copy['Date'].astype(datetime.date))
    
    plot_historical_volume(df)
    
    dataAr = [tuple(x) for x in df_copy[['Date', 'Open', 'Close', 'High', 'Low']].to_records(index = False)]
    fig = plt.figure()
    ax = plt.subplot(1, 1, 1)
    candlestick_ohlc(ax, dataAr, width=0.4, colorup='#77d879', colordown='#db3f3f')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.title(str(ticker).upper() + ' Candlestick Movement from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    plt.ylabel('Price') 
    plt.xlabel('Date')
    plt.show()
    
    description = 'A candlestick is a type of price chart that displays the high, low, open and closing prices of a security'
    description += ' for a specific period. The wide part of the candlestick is called the "real body" '
    description += 'and tells investors whether the closing price was higher or lower than the opening price '
    description += 'with red if the stock closed lower, orange if the stock closed higher. This chart should be used '
    description += 'in conjunction with the historical volume graph to better gauge market sentiment.'
    
    print(description)

def plot_max_drawdown(df):
    '''
    Takes in dataframe with high and low stock price, and returns a max daily drawdown plot with rolling window of 7.
    '''
    
    for i in range(len(tickers_df_list)):
        df_copy = tickers_df_list[i].copy(deep = True)
        Roll_Max = df_copy['Adj Close'].rolling(window=7).max()
        Daily_Drawdown = df_copy['Adj Close']/Roll_Max - 1.0
        Max_Daily_Drawdown = Daily_Drawdown.rolling(window=7).min() 
        
        plt.rcParams['figure.figsize'] = [15, 10]
        plt.ylim(-1, 0.1)
        plt.xlim(start_, end_)
        plt.plot(df_copy['Date'], Max_Daily_Drawdown, label = tickers[i])  
    if len(tickers) == 1:
        plt.title(str(ticker).upper() + ' Max_Daily_Drawdown from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
    elif len(tickers) > 1:
        string = ' & '.join(tickers)
        plt.title(string.upper() + ' Max_Daily_Drawdown from ' + str(start_)[0:11] + 'to ' + str(end_)[0:11])
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
        "Choose One Type of Graph",
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

selection = widgets.Dropdown(description="Pick Graph: ")
selection.options = OPTIONS
display(selection)

#create a button that can plot user's desired graph(s) on command

def on_button_clicked(b):
    graph = selection.value
    if graph == OPTIONS[1]:
        for i in tickers_df_list: 
            plot_historical_prices(i)
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
        for i in tickers_df_list: 
            plot_candlestick(i)
    elif graph == OPTIONS[8]:
        for i in tickers_df_list: 
            plot_Point_and_Figure(i)
    elif graph == OPTIONS[9]:
        plot_max_drawdown(df)
    elif graph == OPTIONS[10]:
        plot_Relative_Strength_Index(df)
        
button = widgets.Button(description = "Visualize")
display(button)

button.on_click(on_button_clicked)
