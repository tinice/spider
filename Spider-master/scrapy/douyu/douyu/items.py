# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    href = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    owner = scrapy.Field()
    num = scrapy.Field()
    week = scrapy.Field()
    all = scrapy.Field()
