# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class flacItem(scrapy.Item):
    href = scrapy.Field()
    song_name = scrapy.Field()
    singer_name = scrapy.Field()
    album = scrapy.Field()
    format = scrapy.Field()
    size = scrapy.Field()
    download_link = scrapy.Field()
    password = scrapy.Field()



