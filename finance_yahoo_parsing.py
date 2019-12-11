import requests
from bs4 import BeautifulSoup as bs
import csv
from time import sleep
from random import uniform

share_list = open('Share_list.txt').read().split('\n')
for share in share_list:
    url = 'https://finance.yahoo.com/quote/' + share + '/history?p=' + share
    r = requests.get(url)
    text = r.text
    soup = bs(text, 'lxml')
    web_data_ = soup.find('table', class_ = 'W(100%) M(0)').find_all('tr', class_ = 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)')[:5]
    web_data = web_data_[::-1]
    with open('Shares_data_1.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = ';')
        print('Data processing of', share)
        writer.writerow(share)
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
            #try:
            #    adj_close = string.find_all('td')[5].find('span').text
            #except:
            #    adj_close = ''
            try:
                volume = string.find_all('td')[6].find('span').text.strip(',')
            except:
                volume = ''

            a = uniform(1,5)
            print(a)
            sleep(a)
            print(date, open, high, low, close, volume)

            writer.writerow( (date, open, high, low, close, volume) )
        del date
        del open
        del high
        del low
        del close
        #del adj_close
        del volume
        f.close()

print('Complited! You are smart guy! You wil get your billions! :D')
