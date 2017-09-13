# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoodsItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    price = scrapy.Field()
    shop_name = scrapy.Field()
    shop_url = scrapy.Field()
    shop_location = scrapy.Field()
    sales = scrapy.Field()

