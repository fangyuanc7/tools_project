#Tools project
import sys
import numpy as np
import pandas as pd

ticker = input("What stock would you like to analyse? ")
print ("You would like to analyze:  " + ticker)



import requests
from bs4 import BeautifulSoup
    
response = requests.get(url)
if not response.status_code == 200:
    return output_list
