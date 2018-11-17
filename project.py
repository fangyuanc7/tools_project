import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
#%matplotlib inline
import pandas_datareader.data as web
import fix_yahoo_finance as yf

ticker = input("What stock would you like to analyse? ")
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

#Add try/except ValueError check here to make sure the input start/end year is within our data bounds 
#i.e. check 1950?<=Year<=2018); 1<=month<=12; 1<=day<=28/30/31

df = web.DataReader([ticker], 'yahoo', start_date, end_date)
print(df.head(10))
