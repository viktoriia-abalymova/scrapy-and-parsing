# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst, Compose
import re


def process_photos(photo):
    try:
        photo = photo.replace('/s/','/b/')
        return photo
    except:
        return photo

def clear_price(value):   #Добавила обработку цены
    value = value.replace('\xa0','').replace('₽','')
    try:
        return(int(value))
    except:
        return(value)


class LeroymerlinItem(scrapy.Item):
    link = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field()
    body = scrapy.Field()
    body_2 = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(clear_price))
    photos = scrapy.Field(input_processor=MapCompose(process_photos), output_processor=TakeFirst())
    _id = scrapy.Field()
