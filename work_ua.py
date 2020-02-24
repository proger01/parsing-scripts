import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import uniform

page = 1
url_data = 'https://www.work.ua/jobs-kharkiv-trainee/?page={0}'.format(page)

r = requests.get(url_data)
soup2 = bs(r.text, 'lxml')
pagination = len(soup2.select('nav ul.pagination.hidden-xs li')) - 2

def info(data):
    for job in data:
        company = job.select('div.add-top-xs span b')[0].text
        vacancy = job.a['title'].split(',')[0]
        date = job.a['title'].split(',')[1]
        print('vacancy: ', vacancy)
        print('date: ', date)
        print('company: ', company)
        print('')

print('\"Trainee\" vacancy')
for i in range(pagination):
    url = 'https://www.work.ua/jobs-kharkiv-trainee/?page={0}'.format(page)
    r = requests.get(url)
    soup = bs(r.text, 'lxml')
    block = soup.select('div.card.card-hover.card-visited.wordwrap.job-link')
    info(block)
    page += 1
    time_out = uniform(1, 4)
    print('time out: ', time_out)
    sleep(time_out)
