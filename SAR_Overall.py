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
    def __init__(self, beginning, end, classifier):
        self.start = beginning
        self.end = end
        self.classifier = classifier

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getClass(self):
        return self.classifier

    def __str__(self):
        return '(' + str(self.start) + ', ' + str(self.end) + ', ' + self.classifier + ')'

    __repr__ = __str__

class SARObject:
    def __init__(self, SARValue, EPValue, AFValue, indexValue, date):
        self.SAR = SARValue
        self.EP = EPValue
        self.AF = AFValue
        self.index = indexValue
        self.date = date

    def getSAR(self):
        return self.SAR

    def getEP(self):
        return self.EP

    def getAF(self):
        return self.AF

    def getIndex(self):
        return self.index

    def getDate(self):
        return self.date

    def modSAR(self, new):
        self.SAR = new

    def modEP(self, new):
        self.EP = new

    def modAF(self, new):
        self.AF = new

    def __str__(self):
        return self.date + '| ' + 'SAR Value: ' + str(self.SAR) + ', Acceleration Factor: ' + str(self.AF)  

    __repr__ = __str__

def nextRisingSAR(SAR, EP, AF, nextindex):
    initialSAR = SAR
    initialEP = EP
    initialAF = AF
    nextAF = initialAF
    
    if(isinstance(initialSAR, str)):
        initialSAR = float(initialSAR.replace(',', ''))

    if(isinstance(initialEP, str)):
        initialEP = float(initialEP.replace(',', ''))

    if HighList[int(nextindex)] > initialEP:
        nextEP = HighList[int(nextindex)]
        if(nextAF < 0.18):
            nextAF = initialAF + 0.02
    else:
        nextEP = initialEP

    if(type(initialSAR) == 'str'):
        initialSAR = float(initialSAR.replace(',', ''))

    if(type(initialEP) == 'str'):
        initialEP = float(initialEP.replace(',', ''))
    
    nextSAR = initialSAR + (initialAF * (initialEP - initialSAR))

    date = DateList[int(nextindex)]
    
    #print(nextSAR)

    #print("---------------------------------")

    nextSARObject = SARObject(nextSAR, nextEP, nextAF, nextindex, date)


##    print(PriceList[nextindex])
##    print(initialEP)
##
##    print(initialAF)
##
##    print(initialSAR)
##    
##    print(nextSARObject)
##
##    print("----------------------------------")

    return nextSARObject

def nextFallingSAR(SAR, EP, AF, nextindex):
    initialSAR = SAR
    initialEP = EP
    initialAF = AF
    nextAF = initialAF

    if(isinstance(initialSAR, str)):
        initialSAR = float(initialSAR.replace(',', ''))

    if(isinstance(initialEP, str)):
        initialEP = float(initialEP.replace(',', ''))

    if LowList[int(nextindex)] < initialEP:
        nextEP = LowList[int(nextindex)]
        if(nextAF < 0.18):
            nextAF = nextAF + 0.02
    else:
        nextEP = initialEP
    
    nextSAR = initialSAR - (initialAF * (initialSAR - initialEP))

    date = DateList[int(nextindex)]
    
    #print(nextSAR)

    #print("---------------------------------")

    nextSARObject = SARObject(nextSAR, nextEP, nextAF, nextindex, date)

##    print(initialEP)
##
##    print(initialAF)
##
##    print(initialSAR)
##    
##    print(nextSARObject)
##
##    print("----------------------------------")
    

    return nextSARObject


##xl = pd.ExcelFile("Data File.csv")
##xl.sheet_names
##
##df = xl.parse("Sheet1")

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

LowList.reverse()
HighList.reverse()
PriceList.reverse()
DateList.reverse()

#print(PriceList)

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
    
LocalHighs = []

lastSwitch = 0

if PriceList[1] > PriceList[0]:
    classifier = "Uptrend"
else:
    classifier = "Downtrend"


LHFound = False

i = 2

while LHFound == False:
    if PriceList[i] > PriceList[i - 1] and PriceList[i] > PriceList[i + 1]:
        LHFound = True
    else:
        i = i + 1

LocalHighs.append(PriceList[i])

#r = Range(0, i, classifier)

#ranges.append(r)

count = 0

while i < len(PriceList):
    if PriceList[i] > PriceList[i - 1] and PriceList[i] > PriceList[i + 1]:
        if classifier == "Uptrend" and PriceList[i] >= LocalHighs[len(LocalHighs) - 1]:
            #print("Stay Uptrend")
            LocalHighs.append(PriceList[i])
            i = i + 1
        if classifier == "Uptrend" and PriceList[i] < LocalHighs[len(LocalHighs) - 1]:
            #print("Switch to Downtrend")
            if i != lastSwitch:
                r = Range(lastSwitch, i, "Uptrend")
                classifier = "Downtrend"
                ranges.append(r)
                LocalHighs.append(PriceList[i])
                lastSwitch = i + 1
                i = i + 1
            else:
                i = i + 1
        if classifier == "Downtrend" and PriceList[i] <= LocalHighs[len(LocalHighs) - 1]:
            #print("Stay Downtrend")
            LocalHighs.append(PriceList[i])
            i = i + 1
        if classifier == "Downtrend" and PriceList[i] > LocalHighs[len(LocalHighs) - 1]:
            #print("Switch to Uptrend")
            if i != lastSwitch:
                r = Range(lastSwitch, i, "Downtrend")
                classifier = "Uptrend"
                ranges.append(r)
                LocalHighs.append(PriceList[i])
                lastSwitch = i + 1
                i = i + 1
            else:
                i = i + 1
    else:
        i = i + 1

#print(ranges)
#Ranges + type in ranges

SARObjectList = []

SAR_InUse = "Rising SAR"

a = 0

while a < len(ranges):
    r = ranges[a]
    if r.getClass() == "Uptrend":
        SAR_InUse = "Rising SAR"
    else:
        SAR_InUse = "Falling SAR"

    if (r.getEnd() - r.getStart()) < 3:
        b = 0
        while b <= (r.getEnd() - r.getStart()):
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart() + b]))
            b = b + 1
    else:
        if SAR_InUse == "Rising SAR":
            StartSAR = LowList[r.getStart() + 3]
            StartEP = max(HighList[r.getStart()], HighList[r.getStart() + 1], HighList[r.getStart() + 2], HighList[r.getStart() + 3])
            StartAF = 0.02
            StartIndex = r.getStart() + 4
            currentIndex = StartIndex
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart()]))
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart() + 1]))
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart() + 2]))
            toAppend = SARObject(StartSAR, StartEP, StartAF, currentIndex - 1, DateList[currentIndex - 1])
            SARObjectList.append(toAppend)
            while currentIndex <= (r.getEnd()):
                SARSource = SARObjectList[len(SARObjectList) - 1]
                #print(SARSource.getAF())
                toAppend = nextRisingSAR(SARSource.getSAR(), SARSource.getEP(), SARSource.getAF(), currentIndex)
                SARObjectList.append(toAppend)
                currentIndex = currentIndex + 1
        else:
            StartSAR = HighList[r.getStart() + 3]
            StartEP = min(LowList[r.getStart()], LowList[r.getStart() + 1], LowList[r.getStart() + 2], LowList[r.getStart() + 3])
            StartAF = 0.02
            StartIndex = r.getStart() + 4
            currentIndex = StartIndex
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart()]))
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart() + 1]))
            SARObjectList.append(SARObject(None, None, None, None, DateList[r.getStart() + 2]))
            toAppend = SARObject(StartSAR, StartEP, StartAF, currentIndex - 1, DateList[currentIndex - 1])
            SARObjectList.append(toAppend)
            while currentIndex <= (r.getEnd()):
                SARSource = SARObjectList[len(SARObjectList) - 1]
                #print(SARSource)
                toAppend = nextFallingSAR(SARSource.getSAR(), SARSource.getEP(), SARSource.getAF(), currentIndex)
                SARObjectList.append(toAppend)
                currentIndex = currentIndex + 1
    a = a + 1


ListOfDates = []
ListOfSARs = []
ListOfAFs = []
                        
j = 0

while j < len(SARObjectList):
    ListOfDates.append(SARObjectList[j].getDate())
    ListOfSARs.append(SARObjectList[j].getSAR())
    ListOfAFs.append(SARObjectList[j].getAF())
    j = j + 1




finaldf = pd.DataFrame({'Date': ListOfDates, 'SAR': ListOfSARs, 'AF': ListOfAFs})

finaldf.to_csv('Output.csv', columns=["Date","SAR","AF"])
