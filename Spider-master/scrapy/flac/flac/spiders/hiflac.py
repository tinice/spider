# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from flac.items import flacItem
from flac.items import flacItem


class HiflacSpider(CrawlSpider):
    name = "hiflac"
    allowed_domains = ["hiflac.com"]

    start_urls = (
        'http://hiflac.com/',
    )
    rules = [
        Rule(LinkExtractor(allow=("http://hiflac.com/music/category/.+")), callback='parse_hiflac', follow=True),
    ]


    def parse_hiflac(self, response):
        element_list = response.css('#primary > div > section > article')
        item_list=[]
        for one in element_list:
            item = flacItem()
            item['href'] = one.css('h2 > a::attr(href)').extract_first()
            request = scrapy.Request(response.urljoin(item['href']),
                                     callback=self.prase_song)
            request.meta['item'] = item
            yield request

    def prase_song(self, response):
        item = response.meta['item']
        element= response.css('#page-header > h1::text').extract_first()
        try:
            item['singer_name'] = element.split('–')[0]
            item['song_name'] = element.split('–')[1].split('.')[0]
            item['format']  = element.split('–')[1].split('.')[1]
            item['download_link'] = response.css('#tabs_0 > h3:nth-child(1) > a::attr(href)').extract_first()
            item['password'] = response.css('#tabs_0 > h3:nth-child(2)').extract_first().replace('提取密码：','')
            item['album'] = 'unknown'
            item['size'] = 'unkown'
        except IndexError as e:
            print(e)
        yield item



if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()