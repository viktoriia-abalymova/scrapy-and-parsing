import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div/a[contains(@href, '/vakansii/')]/@href").extract()

        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)
#очень сомневаюсь на счет кнопки дальше
        next_page = response.xpath("//span[contains(text(),'Дальше')]").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        # добавила ссылку
        link = response.url
        name = response.xpath("//h1/text()").extract()
        #оставила в name extract, потому что extract_first() собирает только первую часть вакансии,
        #иногда на суперджобе у них есть в названии слово в скобках и тогда оно не собирается
        salary = response.xpath("//span[@class = '_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        site = 'https://www.superjob.ru/'
        yield JobparserItem(link=link, name=name, salary=salary, site=site)