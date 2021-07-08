from bs4 import BeautifulSoup, Comment
import requests
import csv

# Easily grab the commented section of the html
def is_comment(element):
    return isinstance(element, Comment)

# Establish the teams and index each one
teams = ["Arizona", "Atlanta", "Baltimore", "Buffalo", "Carolina", "Chicago", "Cincinnati", "Cleveland", "Dallas",
         "Denver", "Detroit", "Green Bay", "Houston", "Indianapolis", "Jacksonville", "Kansas City", "Las Vegas",
         "Los Angeles Chargers", "Los Angeles Rams", "Miami", "Minnesota", "New England", "New Orleans",
         "New York Giants", "New York Jets", "Philadelphia", "Pittsburgh", "San Francisco", "Seattle", "Tampa Bay",
         "Tennessee", "Washington"]
keys = {"Arizona": 0, "Atlanta": 1, "Baltimore": 2, "Buffalo": 3, "Carolina": 4, "Chicago": 5,
        "Cincinnati": 6, "Cleveland": 7, "Dallas": 8, "Denver": 9, "Detroit": 10, "Green Bay": 11,
        "Houston": 12, "Indianapolis": 13, "Jacksonville": 14, "Kansas City": 15, "Las Vegas": 16,
        "Los Angeles Chargers": 17, "Los Angeles Rams": 18, "Miami": 19, "Minnesota": 20, "New England":
        21, "New Orleans": 22, "New York Giants": 23, "New York Jets": 24, "Philadelphia": 25,
        "Pittsburgh": 26, "San Francisco": 27, "Seattle": 28, "Tampa Bay": 29, "Tennessee": 30,
        "Washington": 31, "Oakland": 16, "San Diego": 17, "St. Louis": 18}
# Write out the top row and category numbers for each statistic
conglomerate = [["TeamName", "Year"]]
for i in range(229):
    conglomerate[0].append(i)
for i in range(10):
    for j in range(32):
        conglomerate.append([teams[j], 2020 - i])
    url = "https://www.pro-football-reference.com/years/"+str(2020-i)+"/"
    headers = {"User-Agent": "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)"}
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    iterations = 0
    for t in soup.findAll("tbody"):
        for r in t.findAll("tr"):
            columnNum = 0
            index = -1
            for a in r.findAll("a"):
                if a.text.rsplit(" ", 1)[0] == "Los Angeles" or a.text.rsplit(" ", 1)[0] == "New York": # Ensure that both words of the two word cities are retrieved
                    index = keys[a.text] + 32*i
                elif a.text.rsplit(" ", 1)[0] == "Washington Football": # Ensure that both words of the two word nickname are retrieved
                    index = keys[a.text.split(" ")[0]] + 32*i
                else:
                    index = keys[a.text.rsplit(" ", 1)[0]] + 32*i
            if index < 0:
                continue
            for d in r.findAll("td"):
                if columnNum == 2:
                    if d["data-stat"] != "ties": # Check if there are any ties in the categories
                        conglomerate[index + 1].append(0)
                try:
                    conglomerate[index + 1].append(float(d.text))
                except ValueError:
                    try:
                        conglomerate[index + 1].append(float(d.text.replace('Own ', '')))
                    except ValueError: # If the data is not a float, convert it to one
                        ph = d.text.split(':')
                        ph = int(ph[0])*60 + int(ph[1])
                        conglomerate[index + 1].append(ph)
                columnNum += 1
    for c in soup.find_all(text=is_comment):
        o = BeautifulSoup(c, features="html.parser")
        for t in o.findAll("tbody"):
            iterations += 1
            if iterations < 4: # Skip to the correct table body
                continue
            for r in t.findAll("tr"):
                index = -1
                for d in r.findAll("td"):
                    if d["data-stat"] == "def_two_pt": # Skip this category due to it not being present every year
                        continue
                    if index < 0:
                        if d.text.rsplit(" ", 1)[0] == "Los Angeles" or d.text.rsplit(" ", 1)[0] == "New York":
                            index = keys[d.text] + 32*i
                        elif d.text.rsplit(" ", 1)[0] == "Washington Football":
                            index = keys[d.text.split(" ")[0]] + 32*i
                        else:
                            index = keys[d.text.rsplit(" ", 1)[0]] + 32*i
                        continue
                    try:
                        conglomerate[index + 1].append(float(d.text))
                    except ValueError:
                        try:
                            conglomerate[index + 1].append(float(d.text.replace('Own ', '')))
                        except ValueError:
                            try:
                                ph = d.text.split(':')
                                ph = int(ph[0]) * 60 + int(ph[1])
                                conglomerate[index + 1].append(ph)
                            except ValueError:
                                try:
                                    conglomerate[index + 1].append(float(d.text.replace('%', '')))
                                except ValueError:
                                    conglomerate[index + 1].append(0)
                                    response = requests.get(url)
    # Retrieve defensive stats
    url = "https://www.pro-football-reference.com/years/"+str(2020 - i)+"/opp.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    iterations = 0
    for t in soup.findAll("tbody", limit=1):
        for r in t.findAll("tr"):
            index = -1
            for d in r.findAll(["a", "td"]):
                if index < 0:
                    try:
                        if d.text.rsplit(" ", 1)[0] == "Los Angeles" or d.text.rsplit(" ", 1)[0] == "New York":
                            index = keys[d.text] + 32*i
                        elif d.text.rsplit(" ", 1)[0] == "Washington Football":
                            index = keys[d.text.split(" ")[0]] + 32*i
                        else:
                            index = keys[d.text.rsplit(" ", 1)[0]] + 32*i
                        continue
                    except KeyError:
                        print(r)
                try:
                    conglomerate[index + 1].append(float(d.text))
                except ValueError:
                    try:
                        conglomerate[index + 1].append(float(d.text.replace('Own ', '')))
                    except ValueError:
                        try:
                            ph = d.text.split(':')
                            ph = int(ph[0]) * 60 + int(ph[1])
                            conglomerate[index + 1].append(ph)
                        except ValueError:
                            try:
                                conglomerate[index + 1].append(float(d.text.replace('%', '')))
                            except ValueError:
                                conglomerate[index + 1].append(0)
                                response = requests.get(url)
    for c in soup.find_all(text=is_comment):
        o = BeautifulSoup(c, features="html.parser")
        for t in o.findAll("tbody"):
            iterations += 1
            if iterations < 4:
                continue
            for r in t.findAll("tr"):
                index = -1
                for d in r.findAll(["a", "td"]):
                    if index < 0:
                        if d.text.rsplit(" ", 1)[0] == "Los Angeles" or d.text.rsplit(" ", 1)[0] == "New York":
                            index = keys[d.text] + 32*i
                        elif d.text.rsplit(" ", 1)[0] == "Washington Football":
                            index = keys[d.text.split(" ")[0]] + 32*i
                        else:
                            index = keys[d.text.rsplit(" ", 1)[0]] + 32*i
                        continue
                    try:
                        conglomerate[index + 1].append(float(d.text))
                    except ValueError:
                        try:
                            conglomerate[index + 1].append(float(d.text.replace('Own ', '')))
                        except ValueError:
                            try:
                                ph = d.text.split(':')
                                ph = int(ph[0]) * 60 + int(ph[1])
                                conglomerate[index + 1].append(ph)
                            except ValueError:
                                try:
                                    conglomerate[index + 1].append(float(d.text.replace('%', '')))
                                except ValueError:
                                    conglomerate[index + 1].append(0)
                                    response = requests.get(url)
    print(len(conglomerate[1])) # Print the length of the data's rows
    for j in range(len(conglomerate)): # Print each row of the data
        print(conglomerate[j])
with open("data.csv", "w+") as file: # Write the data to a csv
    csvWriter = csv.writer(file, delimiter=",")
    csvWriter.writerows(conglomerate)
