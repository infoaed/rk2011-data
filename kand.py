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

j=0

def validate_mobile(value):
    rule = re.compile(r'^[0-9 +-,]+$')
    return rule.search(value) is not None

def validate_email(value):
    rule = re.compile(r'^.+@.+$')
    return rule.search(value) is not None

    
for i in data:
    j+=1
    #if j>10: break
    url=("https://rk2019.valimised.ee/et/candidates/candidate-%d.html") % i
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
    dist = soup.find_all("span", {"class", "breadcrumb-item active"})
    #print(dist)
    ringkond = dist[0].text.split(" ")[-1]
    candname = soup.find_all("span", {"class", "uppercase"})
    nimi = candname[0].text.title()
    

    table = soup.find(name='tbody')
    if table is None:
        print("%d: " % i)
        continue;
    rows = table.find_all('tr')
    res = [i, ringkond, nimi]
    mob = ""
    email = ""
    addr = ""
    for row in rows:
        cols = row.find_all('td')
        raw=cols[0].text
#       print(raw)
        if len(raw)==0:
            continue;
#        res = [raw, cols[1].text]
        if raw.strip()=="Kontaktandmed:":
            kont = cols[1].text.strip().split('\xa0')
            for k in kont:
                if validate_mobile(k):
                    mob = k.strip()
                elif validate_email(k):
                    email = k.strip()
                else:
                    addr = k.strip()
        else:
            res.append(cols[1].text.strip())



#        for col in cols:
#            k+=1
#            raw=col.text
#            if len(raw)==0 or raw in ["Andmed"]:
#                break;
#            print(raw)
#            if k==2: break
    
    #print(nimi)
    if len(kont) > 3:
        print (nimi, len(kont), kont)


#    for k in kont:
#        if validate_mobile(k):
#            print(" > " + k)
#        elif validate_email(k):
#            print(" = " + k)
#        else:
#            print(" & " + k.strip())

    res.append(mob)
    res.append(email)
    res.append(addr)
    #print(res)
    with open('rk2019-kandidaadid.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(res)
    csv_file.close()

