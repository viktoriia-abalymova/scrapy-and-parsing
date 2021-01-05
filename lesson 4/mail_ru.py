import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url = 'https://news.mail.ru/'

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//li[@class='list__item']")

news = []
for item in items:
    new_n = {}
    title = item.xpath(".//span[@class='link__text']/text()")
    link = item.xpath(".//a/@href")
    time = item.xpath(".//span[contains(@class, 'note__text')]/@datetime")
    from_where = item.xpath("//a[@class='link color_gray breadcrumbs__link']/@href")

    new_n['time'] = time
    new_n['title'] = title
    new_n['link'] = link
    new_n['from_where'] = from_where
    news.append(new_n)


#Запись в базу данных
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news
news_db.insert_many(news)

pprint(news)

