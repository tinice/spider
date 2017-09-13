# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie80SItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img = scrapy.Field()
    short_description = scrapy.Field()
    long_description = scrapy.Field()
    download_link = scrapy.Field()
    pass
