# -*- coding: utf-8 -*-
import scrapy
import json


class MyItem(scrapy.Item):
    href = scrapy.Field()
    song_name = scrapy.Field()
    singer_name = scrapy.Field()
    album = scrapy.Field()
    format = scrapy.Field()
    size = scrapy.Field()
    download_link = scrapy.Field()
    password = scrapy.Field()


class XicxiSpider(scrapy.Spider):
    name = "xicxi2"
    data = []

    def start_requests(self):
        with open('data_0.json', 'r') as fobj:
            urls = json.load(fobj)
        with open('data_1.json', 'r') as fobj:
            urls += json.load(fobj)
        self.log(len(urls))
        for url in urls:
            item = MyItem(url)
            request = scrapy.Request(url='http://www.xicxi.com'+url['href'], callback=self.parse)
            request.meta['item'] = item
            yield request

    # parse_links
    def parse(self, response):
        self.log(response.url)
        item = response.meta['item']
        item['download_link'] = response.css('#main > div.soft_content > div > div.viewbox > div.cnt > '
                                             'div.content > ul > li > a::attr(href)').extract_first()
        item['password'] = response.css('#main > div.soft_content > div > div.viewbox > div.cnt > div.content > '
                                       'ul > span::text').extract_first().split('：')[-1]
        self.data.append(dict(item))

    def closed(self, reason):
        self.log(len(self.data))
        with open('result_0.json','w') as fobj:
            json.dump(self.data,fobj)
        self.log(reason)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
