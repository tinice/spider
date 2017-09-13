# -*- coding: utf-8 -*-
import scrapy
import json
from furl import furl
from scrapy import Request
from pybloom import BloomFilter


class InfoSpider(scrapy.Spider):
    name = "info"
    allowed_domains = ["maoyan.com"]
    f = furl('http://api.maoyan.com/mmdb/search/movie/tag/list.json?')
    arg = {'cityId': '30', 'limit': '100', 'offset': '0',
           'catId': '1', 'sourceId': '-1', 'yearId': '1',
           'sortId': '3', 'token': '', 'utm_campaign': 'AmovieBmovieCD-1',
           'movieBundleVersion': '7911', 'utm_source': 'Oppo', 'utm_medium': 'android', 'utm_term': '7.9.1',
           'utm_content': '860046034572018', 'ci': '30', 'net': '255', 'dModel': 'ONEPLUS%20A3000',
           'uuid': '3957877BBCA515101B23ABC3B14C92D2364184F6E53440B4AC51D7A07F1A66C0',
           'lat': '22.517843', 'lng': '113.927976',
           '__reqTraceID': '-3215211998383486358',
           'refer': '%2FWelcome', '__skck': '6a375bce8c66a0dc293860dfa83833ef',
           '__skts': '1494730478439', '__skua': '32bcf146c756ecefe7535b95816908e3',
           '__skno': '850436dd-1aa4-4ec2-a9e0-6ab692451da5', '__skcy': 'qruvP88XqHcVBFvc3UAJdmBVahI%3D'}
    f.add(args=arg)
    filter = BloomFilter(capacity=1000000, error_rate=0.001)

    def start_requests(self):
        catId_list = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 100)
        sourceId_list = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 17, 19, 20, 21, 100)
        for yearId in range(1, 14):
            self.f.args['yearId'] = str(yearId)
            for catId in catId_list:
                self.f.args['catId'] = catId
                for sourceId in sourceId_list:
                    self.f.args['sourceId'] = sourceId
                    for one in range(0, 50):
                        self.f.args['offset'] = str(one * 100)
                        yield Request(url=self.f.url)

                        # self.f.args['sourceId'] = str(100)
                        # for one in range(0, 20):
                        #     self.f.args['offset'] = str(one * 50)
                        #     yield Request(url=self.f.url)

    def parse(self, response):
        res = json.loads(response.text)
        for one in res['list']:
            if one['id'] not in self.filter:
                self.filter.add(one['id'])
                yield one
            else:
                self.logger.error('Dup')


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()


