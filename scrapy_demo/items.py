# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PlayerItem(scrapy.Item):
    image = scrapy.Field()
    details = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
    clubs = scrapy.Field()
    palmares = scrapy.Field()
    statistics = scrapy.Field()
