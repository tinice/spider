# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img = scrapy.Field()  # 图片地址
    url = scrapy.Field()  # 商品地址
    shop = scrapy.Field()  # 店家地址
    is_jd = scrapy.Field()  # 是否京东自营
    SkuId = scrapy.Field()  # 产品id
    CommentCount = scrapy.Field()  # 评论总数
    AverageScore = scrapy.Field()  # 平均评价分
    GoodRate = scrapy.Field()  # 好评率
    GeneralRate = scrapy.Field()  # 中评率
    PoorRate = scrapy.Field()  # 差评率
