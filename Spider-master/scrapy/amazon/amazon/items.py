# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    href = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    translator = scrapy.Field()
    price = scrapy.Field()
    discount = scrapy.Field()
    publisher = scrapy.Field()
    score = scrapy.Field()
    comment_num = scrapy.Field()
    time = scrapy.Field()
