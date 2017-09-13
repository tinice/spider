# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter
from os import listdir
from os.path import isfile, join,dirname


class JsonExportPipeline(object):
    def __init__(self):
        path = dirname(__file__)
        file = (f for f in listdir(path) if isfile(join(path,f)))
        max_count = 0
        for one in file:
            if '.json' in one:
                tmp = one.replace('.json','')
                tmp = int(tmp.split('_')[1])
                max_count = tmp if tmp > max_count else max_count
        self.files = {}
        self.count = max_count
        self.file_count = 0
        self.exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('info_{}.json'.format(self.file_count), 'a+b')
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
