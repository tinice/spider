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


class MongoDBDoubanPipline(object):
    def open_spider(self, spider):
        url = 'mongodb://poluo:poluo123@127.0.0.1:27017/proxy'
        self.client = pymongo.MongoClient(url)
        self.db = self.client.proxy
        self.collection_movie = self.db.douban_movie2
        self.collection_actress = self.db.douban_actress

    def process_item(self, item, spider):
        if 'subject' in item['url']:
	        self.collection_movie.insert(dict(item))
        elif 'celebrity' in item['url']:
            self.collection_actress.insert(dict(item))
        else:
            pass

    def close_spider(self, spider):
        self.client.close()
