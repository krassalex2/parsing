# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def process_price(value):
    money = 0
    currency = ''
    if value:
        money = int(value[0].replace(' ', ''))
        currency = value[1]
    return {'money': money, 'currency': currency}


def process_name(value):
    # Возможно здесь можно было использовать output_processor=Join
    # Но здесь еще дополнительно добавил strip
    return ''.join(value).strip()


def process_photos(value):
    return list(['https://www.castorama.ru' + photo for photo in value])


class CatalogParserItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(process_photos))
