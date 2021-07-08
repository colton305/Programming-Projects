from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from numpy import genfromtxt
import requests
import openpyxl
from openpyxl import workbook
from classes import *
import csv
import lxml
from lxml import html


stockSymbol = []
order = []
# Create a list of 90 most traded stocks
for i in range(90):
    order.append(str(i))
headers = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
response = requests.get("https://ca.finance.yahoo.com/most-active?offset=0&count=100")
soup = BeautifulSoup(response.content, features="html.parser")
for t in soup.findAll('tbody'):
    for r in t.findAll('tr'):
        for a in r.findAll('a'):
            stockSymbol.append(a.text)
response = requests.get("https://companiesmarketcap.com/canada/largest-companies-in-canada-by-market-cap/")
soup = BeautifulSoup(response.content, features="html.parser")
for t in soup.findAll('tbody'):
    for r in t.findAll('tr'):
        for d in r.findAll('div', {"class": "company-code"}):
            if ".TO" not in d.text:
                stock = d.text + ".TO"
                if stock not in stockSymbol:
                    stockSymbol.append(stock)
            else:
                if d.text not in stockSymbol:
                    stockSymbol.append(d.text)
stockSymbol += ["VSP.TO", "XQQ.TO", "BTCG.UN.TO"]
print(stockSymbol)
print(len(stockSymbol))
writer = pd.ExcelWriter("Candlestick.xlsx")

csvFile = open('stockTarget.csv', mode='w')
fieldnames = ["StockSymbol", "TargetPrice", "MaxHold", "Stop-Loss", "RSI", "Pattern"]
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
csvWriter.writeheader()

# Iterate through the list
for i in range(len(stockSymbol)):
    date = []
    opening = []
    high = []
    low = []
    close = []
    num = []
    iterations = 0
    dOffset = 0
    skip = False

    # Scrape relevant stock data from each item in the list
    response = requests.get("https://ca.finance.yahoo.com/quote/"+stockSymbol[i]+"/history?p="+
                            stockSymbol[i],
                            headers=headers)
    print("https://ca.finance.yahoo.com/quote/"+stockSymbol[i]+"/history?p="+
                            stockSymbol[i])
    soup = BeautifulSoup(response.content, features="html.parser")
    try:
        '''for t in soup.findAll('tbody'):
            for r in t.findAll('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'):
                for d in r.findAll('span', attrs={"data-reactid": str(53 + iterations*15 - dOffset*8)}):
                    date.append(d.text)
                    if iterations > 0:
                        if date[iterations] == date[iterations - 1]:
                            dOffset += 1
                            skip = True
                if skip is True:
                    skip = False
                    iterations += 1
                    print(55 + iterations*15 - dOffset*8)
                    continue
                for o in r.findAll('span', attrs={"data-reactid": str(55 + iterations*15 - dOffset*8)}):
                    if "," in o.text:
                        sep = o.text.split(",")
                        print(sep)
                        opening.append(float(sep[0])*1000 + float(sep[1]))
                    else:
                        opening.append(float(o.text))
                for h in r.findAll('span', attrs={"data-reactid": str(57 + iterations*15 - dOffset*8)}):
                    if "," in h.text:
                        sep = h.text.split(",")
                        high.append(float(sep[0])*1000 + float(sep[1]))
                    else:
                        high.append(float(h.text))
                for l in r.findAll('span', attrs={"data-reactid": str(59 + iterations*15 - dOffset*8)}):
                    if "," in l.text:
                        sep = l.text.split(",")
                        low.append(float(sep[0])*1000 + float(sep[1]))
                    else:
                        low.append(float(l.text))
                for c in r.findAll('span', attrs={"data-reactid": str(61 + iterations*15 - dOffset*8)}):
                    if "," in c.text:
                        sep = c.text.split(",")
                        close.append(float(sep[0])*1000 + float(sep[1]))
                    else:
                        close.append(float(c.text))
                iterations += 1'''
        element = html.fromstring(response.content)
        table = element.xpath("//table")
        tree = lxml.etree.tostring(table[0], method="xml")
        panda = pd.read_html(tree)
        panda = panda[0].values.tolist()
        print(panda)
        for j in range(0, len(panda) - 1):
            if "-" in panda[j] or any("Dividend" in s for s in panda[j]) or any("Split" in s for s in panda[j]):
                continue
            date.append(panda[j][0])
            if "," in panda[j][1]:
                sep = panda[j][1].split(",")
                opening.append(float(sep[0]) * 1000 + float(sep[1]))
            else:
                opening.append(float(panda[j][1]))
            if "," in panda[j][2]:
                sep = panda[j][2].split(",")
                high.append(float(sep[0]) * 1000 + float(sep[1]))
            else:
                high.append(float(panda[j][2]))
            if "," in panda[j][3]:
                sep = panda[j][3].split(",")
                low.append(float(sep[0]) * 1000 + float(sep[1]))
            else:
                low.append(float(panda[j][3]))
            if "," in panda[j][4]:
                sep = panda[j][4].split(",")
                close.append(float(sep[0]) * 1000 + float(sep[1]))
            else:
                close.append(float(panda[j][4]))
    except (IndexError, ValueError, TypeError):
        print("ERROR:", stockSymbol[i])
        continue
    # Trim each scraped array to length = 90
    print(opening)
    date = date[:90]
    print(date)
    opening = opening[:90]
    opening.reverse()
    print(opening)
    high = high[:90]
    high.reverse()
    print(high)
    low = low[:90]
    low.reverse()
    print(low)
    close = close[:90]
    close.reverse()
    print(close)
    # Ensure that all arrays are at the maximum length, otherwise skip the current symbol
    if len(opening) < 90 or len(high) < 90 or len(low) < 90 or len(close) < 90:
        print("LENGTH ERROR:", stockSymbol[i])
        continue
    direction = estTrends(high, low, close) # Determine the trend direction for every data-point
    cutoff = checkTrends(direction) # Determine the where to begin the trend-lines based off trend direction
    print(cutoff)
    # Perform a linear regression to calculate the slope of each scatter-plot
    lrh = linearRegression(cutoff, high, "high")
    lrl = linearRegression(cutoff, low, "low")
    highAdj = []
    lowAdj = []
    # Create a set of data-points based on the calculated slope in order to draw the line on an excel graph
    for j in range(90):
        highAdj.append(lrh[0] * j + lrh[1])
        lowAdj.append(lrl[0] * j + lrl[1])
    # Check if the slope is nearly horizontal for chart classification
    hzh = checkHz(high, lrh[0])
    hzl = checkHz(low, lrl[0])
    # Check if the slopes are nearly parallel for chart classification
    pl = checkPl(cutoff, high, low, lrh[0], lrl[0])
    hs = headCheck(cutoff, direction, high, close, low)
    dt = dtCheck(cutoff, direction, high, close, low)
    try:
        temp = rsiCalc(cutoff, close)
        rsi = temp[0]
        maxHold = temp[1]
    except ZeroDivisionError:
        continue
    try:
        # Convert all collected data to a pandas dataframe
        data = pd.DataFrame({"Date": order, "Open": opening, "High": high, "Low": low, "Close": close,
                                 "High Adj.": highAdj, "Low Adj.": lowAdj, "RSI": rsi})
        print(stockSymbol[i])
        print(data)
        data.to_excel(writer, stockSymbol[i]) # Print all data in an excel spreadsheet
        # Classify each chart as one of 6 chart types in order to determine positions and set target prices in addition
        # to stop-losses
        target = 0
        stopLoss = 0
        pattern = ""
        if lrh[0] < 0 and lrl[0] > 0:
            print("Pennant")
            target = lrh[0]*90 + lrh[1] + 0.01
            stopLoss = lrl[0]*cutoff + lrl[1]
            pattern = "pennant"
        elif pl:
            print("Flag")
            target = lrh[0]*90 + lrh[1] + 0.01
            stopLoss = lrl[0]*90 + lrl[1]
            pattern = "flag"
        elif hzh is True and lrl[0] > 0:
            print("Ascending Triangle")
            target = lrh[0] * 90 + lrh[1] + 0.01
            stopLoss = lrl[0]*cutoff + lrl[1]
            pattern = "ascending triangle"
        elif hzl is True and lrh[0] < 0:
            print("Descending Triangle")
            target = 100000
            pattern = "descending triangle"
        elif lrh[0] - lrl[0] > 0:
            print("Symmetrical Triangle")
            target = lrh[0] * 90 + lrh[1] + 0.01
            stopLoss = target - 0.02
            pattern = "symmetrical triangle"
        else:
            print("Wedge")
            target = lrh[0] * 90 + lrh[1] + 0.01
            stopLoss = target - 0.02
            pattern = "wedge"
        if hzh is True or hzl is True:
            print("Horizontal")
        if hs[0]:
            print("Head and shoulders")
        if dt[0]:
            print("Double top")
        csvFile = open('stockTarget.csv', mode='a')
        csvWriter.writerow({"StockSymbol": stockSymbol[i], "TargetPrice": target, "MaxHold": maxHold,
                            "RSI": rsi[89], "Pattern": pattern})
    except ValueError or IndexError:
        print("Error:", stockSymbol[i])

writer.save() # Save the excel spreadsheet
csvFile.close()
