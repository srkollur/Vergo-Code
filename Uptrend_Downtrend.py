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

class Range:
    def __init__(beginning, end, classifier):
        self.start = beginning
        self.end = end
        self.classifier = classifier

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getClass(self):
        return self.classifier


xl = pd.ExcelFile("Bitcoin Price History  BTC USD Historical Rates - Investing.com")
xl.sheet_names

df = xl.parse("Sheet1")

Low_df = df['Low']
High_df = df['High']
Price_df = df['Price']

ranges = []

LowList = Low_df.values.tolist()
HighList = High_df.values.tolist()
PriceList = Price_df.values.tolist()

LocalHighs = []

temp1 = 0
temp2 = 0
classifier = "Uptrend"

if PriceList[1] > PriceList[0]:
    classifier = "Uptrend"
else:
    classifier = "Downtrend"

LHFound = False

i = 2

while LHFound = False:
    if PriceList[i] > PriceList[i - 1] and PriceList[i] > PriceList[i + 1]:
        LHFound = True
    else:
        i = i + 1

LocalHighs.append(PriceList[i])

while i < len(PriceList) - 2:
    if PriceList[i] > PriceList[i - 1] and PriceList[i] > PriceList[i + 1]:
        if classifier = "Uptrend" and PriceList[i] > LocalHighs[len(LocalHighs) - 1]:
            LocalHighs.append(PriceList[i])
            i = i + 1
        if classifier = "Uptrend" and PriceList[i] < LocalHighs[len(LocalHighs) - 1]:
            temp2 = i
            r = Range(temp1, temp2, classifier)
            ranges.append(r)
            LocalHighs.append(PriceList[i])
            temp1 = temp2
            classifier = "Downtrend"
            i = i + 1
        if classifier = "Downtrend" and PriceList[i] < LocalHighs[len(LocalHighs) - 1]:
            LocalHighs.append(PriceList[i])
            i = i + 1
        if classifier = "Downtrend" and PriceList[i] > LocalHighs[len(LocalHighs) - 1]:
            temp2 = 1
            r = Range(temp1, temp2, classifier)
            ranges.append(r)
            LocalHighs.append(PriceList[i])
            temp1 = temp2
            classifier = "Uptrend"
            i = i + 1
    else:
        i = i + 1













