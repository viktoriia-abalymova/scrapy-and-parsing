import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news = db.news

#Функция, которая создает базу данных
def db_news(title, time, from_where, link):
    news.insert_one({'title': title,
                     'time': time,
                     'link': link,
                     'from_where': from_where})

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url = 'https://yandex.ru/news/'

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//a[@class='mg-card__link']")

news = []
for item in items:
    new_n = {}
    title = item.xpath(".//h2[@class='mg-card__title']/text()")
    time = item.xpath(".//span[@class='mg-card-source__time']//@datetime")
    link = item.xpath(".//a[@class='mg-card__link']//@href")
    from_where = item.xpath(".//span[@class='news-story__subtitle-text']/text()")

    new_n['title'] = title
    new_n['time'] = time
    new_n['link'] = link
    new_n['from_where'] = from_where
    news.append(new_n)

pprint(news)
