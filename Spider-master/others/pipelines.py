# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import CsvItemExporter


class JsonExportPipeline(object):
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
        file = open('jd_{}.json'.format(self.file_count), 'w+b')
        self.files[spider] = file
        self.exporter = JsonLinesItemExporter(file)
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
            self.spider_closed()
            self.spider_opened()
        self.exporter.export_item(item)
        return item


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
            self.spider_closed()
            self.spider_opened()
        self.exporter.export_item(item)
        return item
