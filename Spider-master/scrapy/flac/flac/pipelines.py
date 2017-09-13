# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem


class JasonFlacPipeline(object):
    def open_spider(self,spider):
        self.file= open('51pae.json','w')

    def process_item(self, item, spider):
        if '娱乐天堂' in item['album']:
            raise DropItem("invalid: %s" % item)
        else:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)



    def close_spider(self,spider):
        self.file.close()

