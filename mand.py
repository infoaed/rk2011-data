#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import random
import requests
import bs4
import string
import csv
import time
import re

min = 101
max = 101+1099
amount = 1099

random.seed(123)

#data = random.sample(range(min, max), amount)
data = range(min, max)

url = "https://rk2019.valimised.ee/et/election-result/acquired-mandates.html"
#print(url)
succ = 1
while succ > 0:
    try:
        page = requests.get(url)
        succ = 0
    except requests.exceptions.RequestException as e:
        print(e)
        succ += 1
        time.sleep(succ)
soup = bs4.BeautifulSoup(page.content, 'lxml')
dist = soup.find_all("table", {"class", "table details table-striped mb-5 d-none d-lg-block"})
#print(dist)
#    ringkond = dist[0].text.split(" ")[-1]
#    candname = soup.find_all("span", {"class", "uppercase"})
#    nimi = candname[0].text.title()

heads = []

table = dist[0].find('thead')
print(table)
hhh = table.find_all("th")
for h in hhh:
    heads.append(h.text)

print(heads)

#exit(1)
j=0
for di in dist:
    j+=1
    table = di.find(name='tbody')
    rrr = table.find_all("tr")
    for r in rrr:
        if r.text.find("Nimekiri kokku") < 0:
            #print(r)
            td = 0
            res = []
            ddd = r.find_all("td")
            for d in ddd:
                if heads[td]=="Jrk nr":
                    print(heads[td], d.text)
                elif heads[td]=="Reg nr":
                    print(heads[td], d.text)
                    res.append(d.text)
                elif heads[td]=="Ringkond":
                    print(heads[td], d.text.title())
                    res.append(d.text.title())
                elif heads[td]=="Kandidaadi nimi":
                    print(heads[td], d.text.title())
                    res.append(d.text.title())
                elif heads[td]=="Hääli kokku":
                    print(heads[td], d.text.strip())
                    res.append(d.text.strip())
                elif heads[td]=="Hääled välisriigist":
                    print(heads[td], d.text)
                    res.append(d.text.strip())
                elif heads[td]=="E-hääled*":
                    print(heads[td], d.text)
                    res.append(d.text.strip())
                else:
                    print(heads[td], d.text)
                td += 1
            if j==1:
                res.append("Isikumandaat")
            elif j==2:
                res.append("Ringkonnamandaat")
            elif j==3:
                res.append("Kompensatsioonimandaat")

            with open('rk2019-mandaadid.csv', 'a') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(res)
            csv_file.close()


