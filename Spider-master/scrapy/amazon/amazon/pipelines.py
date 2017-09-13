# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class JasonAmazonPipeline(object):
    def open_spider(self, spider):
        self.file_num = 0
        self.count = 0
        self.file = open('book_{}.json'.format(self.file_num), 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        if self.count < 10000:
            self.count += 1
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        else:
            self.file.close()
            self.file_num += 1
            self.file = open('book_{}.json'.format(self.file_num), 'w+', encoding='utf-8')
            self.count = 0

    def close_spider(self, spider):
        self.file.close()
