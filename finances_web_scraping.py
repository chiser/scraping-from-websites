# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:28:37 2019

@author: chiser
"""

import bs4 as bs
import requests
import lxml.html as lh
import pandas as pd
import numpy as np

baseurl = 'https://www./aktien/'
sufixurl = '-aktie/historische-kurse'
aktien= ['wirecard','alteryx-registered-a','nel','evotec','amazon','microsoft','apple','hypoport','netflix']

fin_data=[]

for aktie in aktien:
    finalurl = baseurl + aktie + sufixurl
    resp = requests.get(finalurl)

    #Store the contents of the website under doc
    doc = lh.fromstring(resp.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
            
    #Check the length of the first 12 rows
    [len(T) for T in tr_elements]
    
    '''        
    #Create empty list
    summary_table=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[2]:
        i+=1
        name=t.text_content()
        print (i,name)
        summary_table.append((name,[]))
    '''
    
    #Create empty list
    year_table=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[7]:
        i+=1
        name=t.text_content()
        #print (i,name)
        year_table.append((name,[]))
        
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(8,28):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=7:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            year_table[i][1].append(data)
            #Increment i for the next column
            i+=1
            
    [len(C) for (title,C) in year_table]
    
    Dict={title:column for (title,column) in year_table}
    df=pd.DataFrame(Dict)

    flattened_table=pd.DataFrame(df.values.flatten())
    naming= []
    #naming.append(df['Jahr']+df.columns)
    for i in df['Jahr']:
        for oo in df.columns:
            naming.append(i+oo)
    flattened_table.index=naming
    
    fin_data.append(flattened_table)
    
#fin_data=pd.DataFrame()
#fin_data[aktie]=flattened_table
#fin_dat2=pd.DataFrame(fin_data, columns= aktien)
#fin_data2=pd.concat([fin_data[0], fin_data[1],fin_data[2],fin_data[3],fin_data[4],fin_data[5],fin_data[6],fin_data[7],fin_data[8],fin_data[9],fin_data[10]],axis=1,sort=True) #pd.DataFrame(fin_data[0])
#fin_data2=pd.concat([fin_data[0:1:len(fin_data)]],axis=1,sort=True) 
fin_data2=pd.concat(fin_data[::1],axis=1,sort=True)

fin_data2.columns=aktien

#import json
#my_json_string = json.dumps(fin_data)

##Dynamically calling name variables according to number
#ind_aktie_data = {}
#k = 0
#while k < 10:
#    ind_aktie_data[k] = fin_data[k]
#    k += 1

#for k,v in ind_aktie_data.items():
#    exec("%s=%s" % (k,v))
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
 
export_csv = fin_data2.to_csv (r'D:\export_finanzen.csv', index = True, header=True) #Don't forget to add '.csv' at the end of the path

#data=pd.read_csv('D:\export_finanzen.csv',index_col=0)        
