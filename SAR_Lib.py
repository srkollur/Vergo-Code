import quandl
import numpy as np
import scipy
import matplotlib.pyplot as plt
import xlsxwriter
import pandas as pd
import datetime
from datetime import datetime
import statistics
import pandas_datareader.data as wb
import talib


df = pd.read_csv('Data File.csv')

Low_df = df['Low']
High_df = df['High']
Price_df = df['Price']
Date_df = df['Date']

ranges = []

LowList = Low_df.values.tolist()
HighList = High_df.values.tolist()
PriceList = Price_df.values.tolist()
DateList = Date_df.values.tolist()

z = 0

while z < len(LowList):
    if isinstance(LowList[z], str):
        LowList[z] = float(LowList[z].replace(',', ''))
    z = z + 1

y = 0

while y < len(HighList):
    if isinstance(HighList[y], str):
        HighList[y] = float(HighList[y].replace(',', ''))
    y = y + 1

x = 0

while x < len(PriceList):
    if isinstance(PriceList[x], str):
        PriceList[x] = float(PriceList[x].replace(',', ''))
    x = x + 1

LowList.reverse()
HighList.reverse()
PriceList.reverse()
DateList.reverse()

Low = np.array(LowList)
High = np.array(HighList)
Close = np.array(PriceList)

SARtoList = (talib.SAR(High, Low, acceleration = 0.2, maximum = 0.20))


SARdf = pd.DataFrame({'SAR': SARtoList,})

SARdf.to_csv('Output_Lib_SAR.csv')


