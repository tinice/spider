# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import CsvItemExporter
from airbnb.items import AirbnbItem, UserItem
import logging as logger


class JsonExportPipeline(object):
    def __init__(self):
        self.files = {}
        self.room_count = 0
        self.user_count = 0
        self.room_file_count = 0
        self.user_file_count = 0
        self.exporter_room = None
        self.exporter_user = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider, mode=0):
        if mode == 1 or mode == 0:
            room_file = open('Airbnb_room_{}.json'.format(self.room_file_count), 'w+b')
            self.files['room'] = room_file
            self.exporter_room = JsonLinesItemExporter(room_file)
            self.exporter_room.start_exporting()

        if mode == 2 or mode == 0:
            user_file = open('Airbnb_user_{}.json'.format(self.user_file_count), 'w+b')
            self.files['user'] = user_file
            self.exporter_user = JsonLinesItemExporter(user_file)
            self.exporter_user.start_exporting()

    def spider_closed(self, spider, mode=0):
        if mode == 1 or mode == 0:
            self.exporter_room.finish_exporting()
            file = self.files['room']
            file.close()

        if mode == 2 or mode == 0:
            self.exporter_user.finish_exporting()
            file = self.files['user']
            file.close()

    def process_item(self, item, spider):
        if isinstance(item, AirbnbItem):
            self.room_count += 1
            if self.room_count > 100000:
                self.room_count = 0
                self.room_file_count += 1
                self.spider_closed(spider, mode=1)
                self.spider_opened(spider, mode=1)
            self.exporter_room.export_item(item)
        elif isinstance(item, UserItem):
            self.user_count += 1
            if self.user_count > 100000:
                self.user_count = 0
                self.user_file_count += 1
                self.spider_closed(spider, mode=2)
                self.spider_opened(spider, mode=2)
            self.exporter_user.export_item(item)
        else:
            logger.info('Some error happened!')


class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}
        self.count = 0
        self.file_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('jd_{}.csv'.format(self.file_count), 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.count += 1
        if self.count > 1000:
            self.count = 0
            self.file_count += 1
            self.spider_closed(spider)
            self.spider_opened(spider)
        self.exporter.export_item(item)
        return item
