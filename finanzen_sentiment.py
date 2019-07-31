# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:45:14 2019

@author: chise
"""

import bs4 as bs
import requests
import lxml.html as lh
import pandas as pd
import numpy as np
import json

#https://www.wallstreet-online.de/aktien/wirecard-aktie/historische-kurse
#'https://www.finanzen.net/aktienkurse'
baseurl = 'https://www.wallstreet-online.de/aktien/'
sufixurl = '-aktie/nachrichten'
aktien= ['wirecard','alteryx-registered-a','nel','evotec','amazon','microsoft','apple','hypoport','netflix']

news_data=[]

for aktie in aktien:
    finalurl = baseurl + aktie + sufixurl
    resp = requests.get(finalurl)

    #Store the contents of the website under doc
    doc = lh.fromstring(resp.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    a_elements = doc.xpath('//tr')
    #a_elements = doc.xpath('//a') these one gets the news but lines are different for different shares
            
    #Check the length of the rows
    #[len(T) for T in a_elements]
    
    '''
    year_table=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in a_elements:
        i+=1
        name=t.text_content()
        print (i,name)
        year_table.append((name,[]))
    '''    
    #Since out first row is the header, data is stored on the second row onwards
    #Create empty list
    news=[]
    for j in range(8,len(a_elements)): #For wirecard range(201,281). 192,261 for Nel
        #T is our j'th row
        T=a_elements[j]
        data=T.text_content()
        news.append(data)
        
    news_clean=[]
    #Iterate through each element of the row
    for i in range(len(news)):
        data=str(news[i]) 
        #Append the data to the empty list of the i'th column
        news_clean.append(data)

    news_data.append(news_clean)

#news_dat=pd.DataFrame.from_records(news_data)    
#news_dat.columns=aktien
news_dic = dict(zip(aktien, news_data))

with open('news_finances.json', 'w') as fp:
    json.dump(news_dic, fp)
'''        
resp = requests.get(finalurl)
soup = bs.BeautifulSoup(resp.text, "html.parser") #'html5lib'
print(soup.prettify())
text_analysis=soup.get_text()
soup.contents
soup.title
soup.tbody
        
hochtief_kurse= soup.find(id="module-hl-1")
ende_jahr= hochtief_kurse.findAll('td', attrs = {'class':'right'})
int(hochtief_kurse.td.text)

all_tables = soup.findAll('table', class_ = 't-data')
print(type(all_tables))
print(len(all_tables))
print(all_tables)
''' 
 
#export_csv = news_dat.to_csv (r'D:\news_finanzen.csv', header=True) #Don't forget to add '.csv' at the end of the path

     