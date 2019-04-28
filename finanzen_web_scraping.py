# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 13:28:37 2019

@author: chise
"""

import bs4 as bs
import requests

class finanzen_crawler():

    def requesting(self, type_):
        baseurl = 'https://www.finanzen.net/'
        if type_ == 'aktien':
            firstpage = baseurl + 'aktienkurse'
        elif type_ == "etf":
            firstpage = baseurl + 'etf'
        else:
            raise ValueError("Unknown type {}".format(type_))
        finalurl = firstpage
#        headers = {
#            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
#                          'AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/56.0.2924.87 Safari/537.36'}
        resp = requests.get(finalurl)
        soup = bs.BeautifulSoup(resp.text, "html.parser")
        print(soup.prettify())
        text_analysis=soup.get_text()
        soup.head.contents
        #soup.title
        #soup.a
        #soup.find(id="link3")
        
        website_links=[]
        maxpage_td = soup.findAll('a')
        for link in soup.find_all('a'):
            print(link.get('href'))
            website_links.append(link.get('href'))
    
        search_page = baseurl[:-1] + website_links[1]
    
        maxpage_a_tag = list(maxpage_td[0].findAll('a'))
        if not maxpage_a_tag:
            maxpage = 1
        elif (maxpage_a_tag[-1].text == "next"):
            maxpage = maxpage_a_tag[-2].text
        else:
            maxpage = maxpage_a_tag[-1].text

        items = 1
        tickerdict = {}
        for page in range(int(maxpage)):
            resp = requests.get(finalurl, headers=headers)
            soup = bs.BeautifulSoup(resp.text, "lxml")
            table = soup.findAll('div', {'class': 'row quotebox'})
            find_all_args = 'a', {'class': 'screener-link-primary'}
            for row in table:
                tickerdict.update(
                    {tickers.text: tickers['href']
                     for tickers in row.findAll(*find_all_args, href=True)})
                items += 20
            finalurl = "{}{}{}".format(firstpage, "&r=", str(items))

        for data in tickerdict.items():
            print(data)


finviz_crawler().requesting('China')