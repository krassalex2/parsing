import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from catalog_parser.items import CatalogParserItem


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['www.castorama.ru']
    base_url = 'https://www.castorama.ru';
    start_urls = ['https://www.castorama.ru/lighting/interior-lighting/']

    def parse(self, response):
        links = response.xpath("//li[contains(@class, 'product-card')]/a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=CatalogParserItem(), response=response)
        loader.add_xpath('name', "//h1[contains(@class, 'product-essential__name')]/text()")
        loader.add_xpath('price', "(//div[contains(@class, 'price-wrapper')])[1]/descendant::span[@class='price']/span/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos',
                         "//img[contains(@class, 'top-slide__img')]/@data-src")

        yield loader.load_item()
