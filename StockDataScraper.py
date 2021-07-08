from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from numpy import genfromtxt
import requests
import openpyxl
from openpyxl import workbook
import csv
import lxml
from lxml import html


stockSymbol = []
order = []
# Create a list of 100 most traded stocks
for i in range(90):
    order.append(str(i))
headers = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
response = requests.get("https://ca.finance.yahoo.com/most-active?offset=0&count=100")
soup = BeautifulSoup(response.content, features="html.parser")
for t in soup.findAll('tbody'):
    for r in t.findAll('tr'):
        for a in r.findAll('a'):
            stockSymbol.append(a.text)
# Add the largest companies by market cap
response = requests.get("https://companiesmarketcap.com/canada/largest-companies-in-canada-by-market-cap/")
soup = BeautifulSoup(response.content, features="html.parser")
for t in soup.findAll('tbody'):
    for r in t.findAll('tr'):
        for d in r.findAll('div', {"class": "company-code"}):
            if ".TO" not in d.text: # Append ".TO" to ensure all symbols appear with the same formatting
                stock = d.text + ".TO"
                if stock not in stockSymbol: # Cross reference the most traded stocks with the largest companies to prevent duplicates
                    stockSymbol.append(stock)
            else:
                if d.text not in stockSymbol:
                    stockSymbol.append(d.text)
stockSymbol += ["VSP.TO", "XQQ.TO", "BTCG.UN.TO"] # Append a few custom stocks
print(stockSymbol) # Print the stock symbols
print(len(stockSymbol)) # Count how many there are
writer = pd.ExcelWriter("Candlestick.xlsx")

# Iterate through the list
for i in range(len(stockSymbol)):
    date = []
    opening = []
    high = []
    low = []
    close = []
    # Scrape relevant stock data from each item in the list
    response = requests.get("https://ca.finance.yahoo.com/quote/"+stockSymbol[i]+"/history?p="+
                            stockSymbol[i], headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")
    try:
        element = html.fromstring(response.content)
        table = element.xpath("//table")
        tree = lxml.etree.tostring(table[0], method="xml")
        panda = pd.read_html(tree)
        panda = panda[0].values.tolist()
        print(panda) # Print the table that was grabbed from the website
        for j in range(0, len(panda) - 1):
            if "-" in panda[j] or any("Dividend" in s for s in panda[j]) or any("Split" in s for s in panda[j]):
                continue # Skip rows with no valuable data
            date.append(panda[j][0])
            if "," in panda[j][1]: # Check if the number is larger than 3 digits and remove the comma
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
    except (IndexError, ValueError, TypeError): # If there are fields that are missing data skip the stock
        print("ERROR:", stockSymbol[i])
        continue
    # Trim and print each scraped array to length = 90
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
    # Convert all collected data to a pandas dataframe
    data = pd.DataFrame({"Date": order, "Open": opening, "High": high, "Low": low, "Close": close})
    print(stockSymbol[i])
    print(data)
    data.to_excel(writer, stockSymbol[i]) # Print all data in an excel spreadsheet
writer.save() # Save the excel spreadsheet
