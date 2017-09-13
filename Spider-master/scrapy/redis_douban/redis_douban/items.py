# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class doubanmovieItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    duration = scrapy.Field()
    release_time = scrapy.Field()
    rate_num = scrapy.Field()
    actress_list = scrapy.Field()
    url = scrapy.Field()
    cover = scrapy.Field()
    playable = scrapy.Field()
    tag = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()


class doubanactressItem(scrapy.Item):
    name = scrapy.Field()
    sex = scrapy.Field()
    birthday = scrapy.Field()
    birthplace = scrapy.Field()
    movie_list = scrapy.Field()
    url = scrapy.Field()
