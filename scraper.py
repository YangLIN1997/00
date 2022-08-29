import requests
import json
import selenium
import pandas as pd
from tqdm import tqdm
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
url = "https://www.armadale.wa.gov.au/community-consultation"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")
soup = BeautifulSoup(html)

results = []
for table in soup.findAll('table',{'class':'views-table cols-2'}):
    label = table.find('h3').get_text()
    links = table.find_all('a')
    for link in links:
        title = link.get_text()
        link=link['href']

        if link[0]!='h':link='https://www.armadale.wa.gov.au'+link
        page = urlopen(link)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        soup2 = BeautifulSoup(html)
        description = []
        try:
            temp = soup2.find('div', {'class':"truncated-description"})
            temp.find_all('p')
            description=[i.get_text() for i in temp.find_all('p')]
            try:
                description=description+[i.get_text() for i in temp.find_all('li')]
            except:pass
        except:
            try:
                temp = soup2.find('div', {'class':"field-item even"})
                temp.find_all('p')
                description=[i.get_text() for i in temp.find_all('p')]
                try:
                    description=description+[i.get_text() for i in temp.find_all('li')]
                except:pass
            except:
                pass
        results.extend([[title,label,link,description]])


df=pd.DataFrame(results,columns=["title","label", "link","description"])
df = df.replace('\n','', regex=True).replace(r'\s+', ' ', regex=True)
df.to_csv("Armadale.csv",index=False)
