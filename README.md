# Pandas Express: Stock Visualization and Analysis

Group Members: Yue Du, Tianyi Lian, Kyle Liu, Jingxian Ruan

Tools for Analytics Section 002

## What is it?

**Pandas Express** is a user-friendly and customizable tool designed to provide the user with a variety of 
stock analysis tools and charts, with simple data visualizations ranging from historical volume and 
log returns to more complicated technical analysis plots such as Candlestick price charts and Relative
Strength Index indicator.

## Main Features
Here are the current visualization and analysis tools that pandas express provides:

  - Historical Prices
  - Log Returns
  - Cumulative Distribution Function
  - Historical Volume
  - Daily Volatility
  - Value at Risk (VaR)
  - Candlestick
  - Point and Figure
  - Max Drawdown
  - Relative Strength Index (RSI)

## Installation Instructions
Clone the repo listed at https://github.com/kkl2129/tools_project. The main file is listed as project.py, and the 
necessary packages that must be installed before usage are listed in requirements.txt. 

Packages used:
  - Numpy
  - Pandas
  - Requests
  - Datetime
  - Matplotlib
  - MPL Finance
  - Pandas_datareader
  - Fix_Yahoo_Finance
  - Tabulate
  - Seaborn
  - Scipy
  - Math
  
## How to use the program
By running the project.py file, the user will be presented with a input area where the user can input their stock to 
be analyzed, the start time period, and the end time period. The user is able to select from a variety of visualization 
tools to help them gauge the current market sentiment and historical movement of the security. Once selected, the respective
chart will be plotted as well as a brief description to help the user interpret the graph.

Pulled from Yahoo Finance, the data consists of the stock's daily time-series with the interday Date, Volume, High, Low, Close, 
and Adjusted Close of the security. Each function has its own docstring indicating which data is necessary for the respective
analysis.

Here is an example walkthrough of using our tool:

1. After cloning the repo, directly run project.py
![Run project.py](https://github.com/kkl2129/tools_project/blob/master/Pic1.png "Run project.py")

2. The program will ask you what security you would like to analyze. Please input an equity ticker.

3. It will then ask if you want to analyze multiple tickers, or stick with only one.

4. The program will ask for a start and end date time period for which you want to analyze.

5. There will be a dropdown menu for you to select which data analysis tools you want to visualize.

6. Please pick one and click 'Visualize'. The graph will appear with a brief description of how to interpret the graph.

7. If you wish, you can continue to select different graphs and they will appear as well.
