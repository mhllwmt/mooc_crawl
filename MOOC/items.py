# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    file_name = scrapy.Field()
    file_type = scrapy.Field()
    file = scrapy.Field()


class MlItem(scrapy.Item):
    course = scrapy.Field()


class TsItem(scrapy.Item):
    file_urls = scrapy.Field()
    file_name = scrapy.Field()
    file = scrapy.Field()