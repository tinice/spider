# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
import logging as logger
from pymongo import ReturnDocument


class MongoPipeline(object):
    collection_name = 'scrapy_items'
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                # mongo_uri=crawler.settings.get('MONGO_URI'),
                # mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
                mongo_uri='mongodb://user:passwd@ip:port/data',
                mongo_db='data'
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.col = self.db.music

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        operations = []
        for song in data['song_list']:
            song['play_list'] = data['url']
            operations.append(UpdateOne({'id':song['id']},{'$addToSet':{'play_list':song['play_list']}},upsert=True))
        self.col.bulk_write(operations,ordered = False)


class JsonExportPipeline(object):
    def __init__(self):
        self.files = {}
        self.count = 0
        self.file_count = 0
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('music_{}.json'.format(self.file_count), 'a+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.count += 1
        if self.count > 10000:
            self.count = 0
            self.file_count += 1
            self.spider_closed(spider)
            self.spider_opened(spider)
        self.exporter.export_item(item)
        return item
