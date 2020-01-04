import requests
from bs4 import BeautifulSoup as bs
from random import uniform
from datetime import datetime as dt
from time import sleep
import pandas as pd

my_file = pd.read_excel('D:\\my_docs\\tr\\list_reiteration.xlsx', header=0, sep='\t')
my_column_of_tickers = my_file['ticker']
list_of_my_ticker = list(my_column_of_tickers)
date = '{0}.{1}.{2}' .format(dt.now().year, dt.now().month, (dt.now().day-1))

page = 0
number_of_pages = int(input('Enter a number of pages I should process:'))
for i in range(number_of_pages):
    url = 'https://finviz.com/screener.ashx?v=171&o=-change&r=' + str(page) + '1'
    r = requests.get(url)
    #content = open('ab.txt').read()
    #soup = bs(content, 'lxml')
    soup = bs(r.text, 'lxml')
    column_of_shares = soup.find_all('a', class_='screener-link-primary')
    for item in column_of_shares:
        try:
            share = item.text
        except:
            share = '-'
        print(share)
        if share in list_of_my_ticker:
            my_file = my_file.append({'date':date, 'ticker':share, 'r_ticker':share}, ignore_index=True)
            print('{0} is in excel' .format(share))
        else:
            my_file = my_file.append({'ticker':share, 'date':date}, ignore_index=True)
            print('{0} IS NOT in excel' .format(share))
        my_file.to_excel('D:\\my_docs\\tr\\list_reiteration.xlsx', header=True, index=False)
    wait = uniform(1,4)
    print('waiting for {0} secs' .format(wait))
    sleep(wait)
    page += 2

print('The task is done')
