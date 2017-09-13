# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem


class SzlianjiaSpider(scrapy.Spider):
    name = "szlianjia"
    allowed_domains = ["sz.lianjia.com"]
    start_urls = (
        'http://sz.lianjia.com/ershoufang/futianqu/',
        'http://sz.lianjia.com/ershoufang/luohuqu/',
        'http://sz.lianjia.com/ershoufang/nanshanqu/',
        'http://sz.lianjia.com/ershoufang/yantianqu/',
        'http://sz.lianjia.com/ershoufang/baoanqu/',
        'http://sz.lianjia.com/ershoufang/longgangqu/',
        'http://sz.lianjia.com/ershoufang/longhuaqu/',
        'http://sz.lianjia.com/ershoufang/dapengxinqu/',
        'http://sz.lianjia.com/ershoufang/pingshanqu/',
        'http://sz.lianjia.com/ershoufang/guangmingxinqu/',
    )
    num = 0

    def parse(self, response):
        self.log('response from {}'.format(response.url))
        data_lsit = response.css('body > div.content > div.leftContent > ul.sellListContent > li')
        for one in data_lsit:
            myitem = LianjiaItem()
            myitem['name'] = one.css('div.info.clear > div.title > a::text').extract_first()
            myitem['url'] = one.css('div.info.clear > div.title > a::attr(href)').extract_first()
            myitem['image'] = one.css('a.img > img::attr(src)').extract_first()
            myitem['address'] = one.css('div.address > div.houseInfo > a::attr(href)').extract_first()
            myitem['info'] = one.css('div.address > div.houseInfo::text').extract_first()
            myitem['follow_info'] = one.css('div.followInfo::text').extract_first()
            myitem['price'] = one.css('div.totalPrice > span::text').extract_first()
            for another_one in one.css('div.tag > span'):
                myitem['tag'] = '/' + another_one.css('::text').extract_first()
            self.num += 1
            yield myitem
        total_num = int(response.css(
            'body > div.content > div.leftContent > div.resultDes.clear > h2 > span::text').extract_first()) / 30
        total_num = total_num if total_num < 100 else 100
        tmp = response.url.find('pg')
        if tmp != -1:
            num = int(response.url[tmp + 2:].replace('/', ''))
            if num + 1 <= total_num:
                next_link = response.url.replace(str(num), str(num + 1))
            else:
                self.log('Final page')
        else:
            next_link = response.url + 'pg2/'
        self.log('next link {}'.format(next_link))
        yield scrapy.Request(next_link, callback=self.parse)

    def closed(self, reason):
        self.log(self.num)
        self.log(reason)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
