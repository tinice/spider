# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from scrapy.exceptions import DropItem


class JasonFlacPipeline(object):
    def open_spider(self, spider):
        self.file = open('template.json', 'w')
        self.used_list = []

    def process_item(self, item, spider):
        if item['href'] not in self.used_list:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            self.used_list.append(item['href'])
        else:
            raise DropItem("already in list: %s" % item)

    def close_spider(self, spider):
        self.file.close()


class MongoDBFlacPipline(object):
    def open_spider(self, spider):
        # url = 'mongodb://xxx:xxx@ip:27017/db_name'
        # self.client = pymongo.MongoClient(url)

        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client.proxy
        self.collection = self.db.template
        self.used_list = []

    def process_item(self, item, spider):
        if item['href'] not in self.used_list:
            self.collection.insert(dict(item))
            self.used_list.append(item['href'])
        else:
            raise DropItem("already in list: %s" % item)

    def close_spider(self, spider):
        self.client.close()
