import requests
from bs4 import BeautifulSoup as bs
from random import uniform
from time import sleep
import pandas as pd

page_var = 0
for item in range(40):
    url_finviz = 'https://finviz.com/screener.ashx?v=111&f=sec_technology&r=' + str(page_var) + '1'
    r = requests.get(url_finviz)
    html = r.text
    soup = bs(html, 'lxml')
    web_data = soup.find('table', {'width' : '100%', 'cellpadding' : '3', 'cellspacing' : '1', 'border' : '0', 'bgcolor' : '#d3d3d3'}).find_all('tr')[1:]
    for string in web_data:
        try:
            ticker = string.find_all('td')[1].text
        except:
            ticker = '-'
        print('Data processing of:', ticker)

        url_ticker = 'https://finviz.com/quote.ashx?t=' + ticker
        r2 = requests.get(url_ticker)
        html2 = r2.text
        soup2 = bs(html2, 'lxml')
        try:
            country = soup2.find_all('td', class_ = 'fullview-links')[1].find_all('a')[2].text
        except:
            country = '-'
        try:
            m_cap = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[1].find_all('td')[1].find('b').text
        except:
            m_cap = '-'
        try:
            income = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[2].find_all('td')[1].find('b').text
        except:
            income = '-'
        try:
            sales = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[3].find_all('td')[1].find('b').text
        except:
            sales = '-'
        try:
            p_e = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[0].find_all('td')[3].find('b').text
        except:
            p_e = '-'
        try:
            p_s = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[3].find_all('td')[3].find('b').text
        except:
            p_s = '-'
        try:
            p_b = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[4].find_all('td')[3].find('b').text
        except:
            p_b = '-'
        try:
            p_c = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[5].find_all('td')[3].find('b').text
        except:
            p_c = '-'
        try:
            p_fcf = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[6].find_all('td')[3].find('b').text
        except:
            p_fcf = '-'
        try:
            beta = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[6].find_all('td')[11].find('b').text
        except:
            beta = '-'
        try:
            price = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[10].find_all('td')[11].find('b').text
        except:
            price = '-'
        try:
            avg_volume = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[10].find_all('td')[9].find('b').text
        except:
            avg_volume = '-'
        try:
            shs_outstand = soup2.find('table', class_ = 'snapshot-table2').find_all('tr')[0].find_all('td')[9].find('b').text
        except:
            shs_outstand = '-'

        try:
            url_f_ya = 'https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
            r3 = requests.get(url_f_ya)
            html3 = r3.text
            soup3 = bs(html3, 'lxml')
            try:
                ev_s = soup3.find('table', class_='table-qsp-stats Mt(10px)').find_all('tr')[7].find_all('td')[1].text
            except:
                ev_s = '-'
            try:
                ev_ebitda = soup3.find('table', class_='table-qsp-stats Mt(10px)').find_all('tr')[8].find_all('td')[1].text
            except:
                ev_ebitda = '-'
        except:
            ev_s = '-'
            ev_ebitda = '-'

        my_file = pd.read_excel('D:\\my_docs\\tr\\m_technology_(16.05.2019).xlsx', header=0, sep='\t')
        my_file = my_file.append({'ticker':ticker, 'm_cap':m_cap, 'income':income, 'sales':sales, 'p_e':p_e, 'p_s':p_s, 'p_b':p_b, 'p_c': p_c, 'p_fcf':p_fcf, 'ev_s':ev_s, 'ev_ebitda':ev_ebitda, 'beta':beta, 'avg_volume':avg_volume, 'price':price, 'shs_outstand':shs_outstand, 'country':country}, ignore_index=True)
        my_file.to_excel('D:\\my_docs\\tr\\m_technology_(16.05.2019).xlsx', header=True, index=False)

        wait = uniform(1,3)
        print('waiting', wait)
        sleep(wait)

    page_var += 2

print('Check file! Data must be there! :D')