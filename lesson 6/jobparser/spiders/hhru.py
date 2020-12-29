import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=Python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='vacancy-serp-item__info']//a/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[contains(@class,'HH-Pager-Controls-Next')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        #добавила ссылку
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//p[@class='vacancy-salary']//span/text()").extract()
        site = 'https://hh.ru/'
        yield JobparserItem(link=link, name=name, salary=salary, site=site)
