# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()           # 课程名
    school = scrapy.Field()         # 开课学校
    teacher = scrapy.Field()        # 主讲老师
    introduction = scrapy.Field()   # 课程介绍
    url = scrapy.Field()            # 课程主页

class ClassItem(scrapy.Item):
    url = scrapy.Field()            # 课程地址
    videos = scrapy.Field()         # 课程视频地址
    caption = scrapy.Field()        # 课程字母
    explanation = scrapy.Field()    # 系统介绍
    resources = scrapy.Field()      # 课程资源
