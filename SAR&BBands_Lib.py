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

# 'Data File.csv' is input file name

Low_df = df['Low']
High_df = df['High']
Price_df = df['Price']
Date_df = df['Date']

#Data File split into separate dataframes

LowList = Low_df.values.tolist()
HighList = High_df.values.tolist()
PriceList = Price_df.values.tolist()
DateList = Date_df.values.tolist()

#converted to list

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

#type conversions complete, string --> float

LowList.reverse()
HighList.reverse()
PriceList.reverse()
DateList.reverse()

#lists reversed, data order changes from 2017-2012 to 2012-2017
#Comment out all .reverse() methods of Data File is already in 2012-2017 order

Low = np.array(LowList)
High = np.array(HighList)
Close = np.array(PriceList)

#Low, High, and Close converted to Array format (TA-Lib calls require Array)

SARtoList = (talib.SAR(High, Low, acceleration = 0.2, maximum = 0.20))
BBandsArray = (talib.BBANDS(Close, timeperiod = 5, nbdevup = 2, nbdevdn = 2, matype = 0))

#method calls to TA-Lib complete, results stored in SARtoList (list) and BBandsArray (array)

BBandsUpperDF = pd.DataFrame(BBandsArray[0], columns = ['Upper Band',])
BBandsMiddleDF = pd.DataFrame(BBandsArray[1], columns = ['Middle Band',])
BBandsLowerDF = pd.DataFrame(BBandsArray[2], columns = ['Lower Band',])

DateDF = pd.DataFrame({'Date': DateList,})

SARdf = pd.DataFrame({'SAR': SARtoList,})

PricesDF = pd.DataFrame({'Date': DateList, 'Price': PriceList, 'High': HighList, 'Low': LowList})

#All data converted to DataFrame type

toCombine = [PricesDF, SARdf, BBandsUpperDF, BBandsMiddleDF, BBandsLowerDF,]

finaldf = pd.concat(toCombine, axis = 1,)

#DataFrames combined

finaldf.to_csv('Output_Lib_SAR and BBands and Prices.csv')

#DataFrames written to csv file output
