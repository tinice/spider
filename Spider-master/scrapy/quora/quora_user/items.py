# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoraItem(scrapy.Item):
    Name = scrapy.Field()
    Num = scrapy.Field()
    
class FollowerItem(scrapy.Item):
    Name = scrapy.Field()
    Work = scrapy.Field()
    School = scrapy.Field()
    Location = scrapy.Field()
    AnswerViews = scrapy.Field()
    PublishedWriter = scrapy.Field()
    FollowersNum = scrapy.Field()
