import requests
from bs4 import BeautifulSoup as bs
import csv
from datetime import datetime as dt
from random import uniform
from time import sleep
import pandas as pd

index = 10

share_list = open('Share_list_15.11.txt').read().split('\n')
for share in share_list:
    url = 'https://finance.yahoo.com/quote/' + share + '/history?p=' + share
    r = requests.get(url)
    text = r.text
    soup = bs(text, 'lxml')
    web_data_ = soup.find('table', class_ = 'W(100%) M(0)').find_all('tr')[5:6]
    web_data = web_data_[::-1]
    print('Data processing of', share)
    for string in web_data:
        try:
            date = string.find_all('td')[0].find('span').text
        except:
            date = ''
        try:
            open = string.find_all('td')[1].find('span').text
        except:
            open = ''
        try:
            high = string.find_all('td')[2].find('span').text
        except:
            high = ''
        try:
            low = string.find_all('td')[3].find('span').text
        except:
            low = ''
        try:
            close = string.find_all('td')[4].find('span').text
        except:
            close = ''
        try:
            volume = string.find_all('td')[6].find('span').text.strip(',')
        except:
            volume = ''

        df = pd.read_excel('D:\\my_docs\\tr\\a_15.11.2019.xlsx', header=0, sep='\t')
        df.Open_price[index] = open
        df.High[index] = high
        df.Low[index] = low
        df.Close_price[index] = close
        df.Volume[index] = volume

        df.to_excel('D:\\my_docs\\tr\\a_15.11.2019.xlsx', header=True, index=False)

        index += 1

        a = uniform(1,7)
        print('Waiting', a, 'sec for next string')
        print(date, open, high, low, close, volume)
        sleep(a)

    index += 10

print('01 DONE!')


