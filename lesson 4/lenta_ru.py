import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

url = 'https://lenta.ru/'

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)

#я делала изначально через item, но буду честной воспользовалась вашей подсказкой из вебинара
#items = dom.xpath('//div[@class="item"]')
items = dom.xpath("//time[@class='g-time']/../..")

news = []
for item in items:
    new_n = {}
    name = item.xpath(".//a/text()")
    time = item.xpath(".//time[@class='g-time']/@datetime")
    link = item.xpath(".//a/@href")


    new_n['name'] = name
    new_n['time'] = time
    new_n['link'] = link
    new_n['from_where'] = url
    news.append(new_n)


#Запись в базу данных
client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news
news_db.insert_many(news)

pprint(news)