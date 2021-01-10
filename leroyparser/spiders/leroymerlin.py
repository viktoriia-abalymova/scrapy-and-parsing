import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroyparser.items import LeroymerlinItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/korpusnaya-mebel/']
    #стартовая ссылка на раздел корпусной мебели,можно оставить несколько стартовых ссылок,если потребуется

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class = 'plp-item__info__title']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.item_parse)
    #переход на след страницу по contains
        next_page = response.xpath("//div[contains(text(),'Посмотреть ещё')/@href]").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def item_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('photos', "//source[contains(@media, '1024px')]/@srcset")
        #не нашла наибольший размер
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('description', "//p/text()")
        #я не уверена на счет этого варианта для сбора характеристики, он срабатывает только при одном xpath пути
        #loader.add_xpath('body', "//div/dd[@class='def-list__definition']/text()" | "//div/dt[@class='def-list__term']/text()")
        loader.add_xpath('body', "//div/dt[@class='def-list__term']/text()")
        loader.add_xpath('body_2', "//div/dd[@class='def-list__definition']/text()")
        loader.add_xpath('price', "//span[@slot = 'price']/text()")
        yield loader.load_item()

#добавить характеристику,как словарь
