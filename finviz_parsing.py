import requests
from bs4 import BeautifulSoup as bs
import csv
from datetime import datetime as dt
from random import uniform
from time import sleep
import pandas as pd

page_var = 0
for item in range(4):
    url_finviz = 'https://finviz.com/screener.ashx?v=171&o=-change&r=' + str(page_var) + '1'
    r = requests.get(url_finviz)
    html = r.text
    #html = open('finviz_html.html').read()
    soup = bs(html, 'lxml')
    web_data_finviz = soup.find('table', {'width' : '100%', 'cellpadding' : '3', 'cellspacing' : '1', 'border' : '0', 'bgcolor' : '#d3d3d3'}).find_all('tr')[3:]
    for string in web_data_finviz:
        try:
            number = string.find_all('td')[0].text
        except:
            number = ''
        try:
            ticker = string.find_all('td')[1].text
        except:
            ticker = ''
        try:
            W52_high = string.find_all('td')[7].text
        except:
            W52_high = ''
        try:
            W52_low = string.find_all('td')[8].text
        except:
            W52_low = ''
        try:
            change = string.find_all('td')[11].text
        except:
            change = ''
        try:
            volume = string.find_all('td')[14].text
        except:
            volume = ''

        wait_1 = uniform(1, 3)
        print(wait_1)
        sleep(wait_1)

        url_finviz2 = 'https://finviz.com/quote.ashx?t=' + ticker
        r_3 = requests.get(url_finviz2)
        text_3 = r_3.text
        soup_3 = bs(text_3, 'lxml')
        mega = 'Mega'
        capitalization = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[1].find_all('td')[1].find('b').text[:-1]
        capitalization_2 = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[1].find_all('td')[1].find('b').text[-1]
        if capitalization_2 == 'B':
            capitalization += mega
        try:
            perf_week = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[0].find_all('td')[11].find('b').text
        except:
            perf_week = ''
        try:
            perf_month = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[1].find_all('td')[11].find('b').text
        except:
            perf_month = ''
        try:
            perf_quarter = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[2].find_all('td')[11].find('b').text
        except:
            perf_quarter = ''
        try:
            perf_half_year = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[3].find_all('td')[11].find('b').text
        except:
            perf_half_year = ''
        try:
            perf_year = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[4].find_all('td')[11].find('b').text
        except:
            perf_year = ''
        try:
            short_float = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[2].find_all('td')[9].find('b').text
        except:
            short_float = ''
        try:
            short_ratio = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[3].find_all('td')[9].find('b').text
        except:
            short_ratio = ''
        web_data_4 = soup_3.find_all('td', class_ = 'fullview-links')[1].find_all('a')
        web_d1 = web_data_4[0].text
        web_d2 = web_data_4[1].text
        industry = web_d1 + ' | ' + web_d2
        #rel_volume = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[-3].find_all('td')[-3].find('b').text
        avg_volume = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[-2].find_all('td')[-3].find('b').text[:-1]
        avg_volume_2 = soup_3.find('table', class_ = 'snapshot-table2').find_all('tr')[-2].find_all('td')[-3].find('b').text[-1]
        if avg_volume_2 == 'M':
            avg_volume += mega
        date = '%s.%s.%s' %((dt.now().day-1), dt.now().month, dt.now().year)

        url_f_yahoo = 'https://finance.yahoo.com/quote/' + ticker + '/history?p=' + ticker
        r_2 = requests.get(url_f_yahoo)
        text_2 = r_2.text
        soup_2 = bs(text_2, 'lxml')
        web_data_2 = soup_2.find('table', class_ = 'W(100%) M(0)').find_all('tr')[:3]
        try:
            previous_close = web_data_2[2].find_all('td')[4].find('span').text
        except:
            previous_close = ''
        try:
            open = web_data_2[1].find_all('td')[1].find('span').text
        except:
            open = ''
        try:
            high = web_data_2[1].find_all('td')[2].find('span').text
        except:
            high = ''
        try:
            low = web_data_2[1].find_all('td')[3].find('span').text
        except:
            low = ''
        try:
            close = web_data_2[1].find_all('td')[4].find('span').text
        except:
            close = ''

        try:
            perc_of_gap = (float(open)/float(previous_close)) - 1
        except:
            perc_of_gap = 0
        try:
            change_tr = (float(close)/float(previous_close)) - 1
        except:
            change_tr = 0
        direct = ''
        if change_tr > perc_of_gap:
            direct = 'up'
        elif change_tr < perc_of_gap:
            direct = 'down'
        else:
            direct = '='
        g_v = ''
        if perc_of_gap < 0.333 * change_tr and perc_of_gap > 0:
            g_v = 'v'
        elif perc_of_gap > 0.333 * change_tr and perc_of_gap < 0.666 * change_tr:
            g_v = 'g+v'
        elif perc_of_gap > 0.666 * change_tr:
            g_v = 'g'
        else:
            g_v = 'v'
        class_of_change = ''
        if change_tr > 0.3:
            class_of_change = 0
        elif change_tr > 0.25 and change_tr <= 0.3:
            class_of_change = 1
        elif change_tr > 0.2 and change_tr <= 0.25:
            class_of_change = 2
        elif change_tr > 0.15 and change_tr <= 0.2:
            class_of_change = 3
        elif change_tr > 0.1 and change_tr <= 0.15:
            class_of_change = 4
        else:
            class_of_change = 5

        my_file = pd.read_excel('D:\\my_docs\\tr\\l_10-30_NEW.xlsx', header=0, sep='\t')
        my_file = my_file.append({'Date':date, 'Ticker':ticker, 'Close_price_before_gap':previous_close, 'Open_price':open, 'High':high, 'Low':low, 'Close_price':close, 'Gap_percent':perc_of_gap, 'Change_from_close_of_gap':0, 'Change_since_last_close_in_gap':change_tr, 'Percent_of_high_from_close_in_gap':'-', 'Percent_of_low_from_close_in_gap':'-', 'Max_HIGH':'-', 'Max_LOW':'-', 'Pre_market':'-', 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry, 'M_cap':capitalization, 'Volume':volume, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':0, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':1, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':2, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':3, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':4, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':5, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':6, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':7, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':8, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':9, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)
        my_file = my_file.append({'Ticker':ticker, 'Gap_percent':perc_of_gap, 'W52_High':W52_high, 'W52_Low':W52_low, 'Perf_week':perf_week, 'Perf_month':perf_month, 'Perf_quarter':perf_quarter, 'Perf_half_year':perf_half_year, 'Perf_year':perf_year, 'Short_float':short_float, 'Short_ratio':short_ratio, 'Industry':industry,  'M_cap':capitalization, 'Avarage_volume_k':avg_volume, 'Days_of_monitoring':10, 'Change_in_zero_day':change_tr, 'Class_of_change':class_of_change, 'Direction_after_open_of_gap':direct, 'Gap_Volume':g_v}, ignore_index=True)

        my_file.to_excel('D:\\my_docs\\tr\\l_10-30_NEW.xlsx', header=True, index=False)

        print(number, date, ticker, change)
        wait = uniform(1,7)
        print(wait)
        sleep(wait)

    page_var += 2

print('l_10_30 Data is done!')
