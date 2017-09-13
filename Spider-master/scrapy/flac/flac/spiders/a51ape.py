# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from flac.items import flacItem


class A51apeSpider(CrawlSpider):
    name = "51ape"
    allowed_domains = ["51ape.com"]
    start_urls = (
        'http://www.51ape.com/',
    )
    rules = [
        Rule(LinkExtractor(allow=("http://www.51ape.com/.+yinyue/")), callback='parse_yinyue', follow=True),
        Rule(LinkExtractor(allow=("/.+yinyue/index")), callback='parse_yinyue', follow=True),
        Rule(LinkExtractor(allow=("/.+yueyu")), callback='parse_yinyue', follow=True),
        Rule(LinkExtractor(allow=("/.+yingwen")), callback='parse_yinyue', follow=True),
        Rule(LinkExtractor(allow=("/.+经典歌曲")), callback='parse_yinyue', follow=True),
        Rule(LinkExtractor(allow=("/.+zhuanji")), callback='parse_zhuanji', follow=True),
    ]

    def parse_yinyue(self, response):
        element_list = response.css('body > div.bg_wh.all.m > div > div.fl.over.w638 > div.fl.over.w638.mt_2 > '
                                    'div.news.w310.over.fl > ul > li')
        item_list = []
        for one in element_list:
            item = flacItem()
            tmp = one.css('a::attr(title)').extract_first()
            try:
                item['singer_name'] = tmp.split('-')[0]
                tmp = tmp.split('-')[1].split('.')
                item['format'] = tmp[1]
            except IndexError:
                continue
            item['href'] = one.css('a::attr(href)').extract_first()
            item['size'] = one.css('span.fr.c999::text').extract_first()
            item_list.append(item)
            request = scrapy.Request(response.urljoin(item['href']),
                                     callback=self.prase_song)
            request.meta['item'] = item
            yield request

    def parse_zhuanji(self, response):
        element_list = response.css('body > div.bg_wh.all.m > div > div.fl.over.w638 > div.fl.over.w638.mt_2 > '
                                    'div.news.over.fl > ul > li')
        item_list = []
        for one in element_list:
            item = flacItem()
            tmp = one.css('a::attr(title)').extract_first()
            try:
                item['singer_name'] = tmp.split('-')[0]
                tmp = tmp.split('-')[1].split('.')
                item['format'] = tmp[1]
            except IndexError:
                continue
            item['href'] = one.css('a::attr(href)').extract_first()
            item['size'] = one.css('span.fr.c999::text').extract_first()
            item_list.append(item)
            request = scrapy.Request(response.urljoin(item['href']),
                                     callback=self.prase_song)
            request.meta['item'] = item
            yield request


    def prase_song(self, response):
        element = response.css('body > div.bg_wh.all.m > div > div.fl.over.w638 > h1::text').extract_first()

        item = response.meta['item']
        item['song_name'] = element.split('-')[1].split('.')[0]
        item['album'] = response.css('body > div.bg_wh.all.m > div > div.fl.over.w638'
                                     ' > h3:nth-child(3)::text').extract_first().replace('选自专辑', '')
        item['download_link'] = response.css('body > div.bg_wh.all.m > div > div.fl.over.w638 '
                                             '> a::attr(href)').extract_first()
        item['password'] = response.css('body > div.bg_wh.all.m > div > div.fl.over'
                                        '.w638 > b').extract_first().split('：')[-1].replace('</b>', '')
        return item


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
