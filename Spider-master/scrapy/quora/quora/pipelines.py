# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import logging as logger


class FollowersPipeline(object):
    def open_spider(self, spider):
        url = 'mongodb://poluo:poluo123@115.28.36.253:27017/proxy'
        client = pymongo.MongoClient(url)
        db = client.proxy
        self.collection = db.quora_user
        self.collection_tmp = db.quora_tmp

    def process_item(self, item, spider):
        result = self.collection.find_one({'Name':item['Name']})
        if not result:
            result = self.collection_tmp.find_one({'Name':item['Name']})
        if result:
            num = result['Num']
            if num > item['Num']:
                logger.info('same data {} less'.format(result))
                pass
            else:
                logger.info('same data {} more'.format(result))
                try:
                    self.collection.remove(result)
                except Exception as e:
                    self.collection_tmp.remove(result)
                    pass
                self.collection.insert(dict(item))
        else:
            logger.info('NO same data {}'.format(item))
            self.collection.insert(dict(item))

    def close_spider(self, spider):
        self.client.close()


class UserPipeline(object):
    def open_spider(self, spider):
        self.file_num = 0
        self.count = 0
        self.file = open('quora_{}.json'.format(self.file_num), 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        if self.count < 10000:
            self.count += 1
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        else:
            self.file.close()
            self.file_num += 1
            self.file = open('quora_{}.json'.format(self.file_num), 'w+', encoding='utf-8')
            self.count = 0

    def close_spider(self, spider):
        self.file.close()
