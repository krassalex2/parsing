import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector import Selector


class MyscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    vacancy_name = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency_salary = scrapy.Field()
    vacancy_link = scrapy.Field()
    _id = scrapy.Field()


class HhRuSpider(scrapy.Spider):

    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://voronezh.hh.ru/vacancies/razrabotchik'
    ]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies = response.css('div.vacancy-serp-item__layout')
        for vacancy in vacancies:
            yield self.parse_vacancy(vacancy, response.url)

    def parse_vacancy(self, vacancy: Selector, url: str):
        vacancy_name = vacancy.css('a::text').get()

        vacancy_salary = vacancy.css('span.bloko-header-section-3::text').get()
        if vacancy_salary:
            min_salary, max_salary, currency_salary = self.clean_salary(vacancy_salary)
        else:
            min_salary, max_salary, currency_salary = None, None, None

        vacancy_link = url

        return MyscrapingItem(
            vacancy_name=vacancy_name,
            min_salary=min_salary,
            max_salary=max_salary,
            currency_salary=currency_salary,
            vacancy_link=vacancy_link
        )

    def clean_salary(self, vacancy_salary_text, min_salary=None, max_salary=None, currency_salary=None):
        list_salary = vacancy_salary_text.replace('\u202f', '').split()
        for i in range(len(list_salary) - 1):
            if list_salary[i] == 'от':
                min_salary = int(list_salary[i + 1])
            elif list_salary[i] == 'до':
                max_salary = int(list_salary[i + 1])
            elif list_salary[i] == '–':
                min_salary = int(list_salary[i - 1])
                max_salary = int(list_salary[i + 1])
        currency_salary = list_salary[-1]

        return min_salary, max_salary, currency_salary


