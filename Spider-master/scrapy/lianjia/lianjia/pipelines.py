# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class LianjiaPipeline(object):
    def open_spider(self, spider):
        url = 'mongodb://poluo:poluo123@localhost:27017/proxy'
        self.client = pymongo.MongoClient(url)
        self.db = self.client.proxy
        self.collection = self.db.szlianjia

    def process_item(self, item, spider):
        self.collection.insert(dict(item))

    def close_spider(self, spider):
        self.client.close()
