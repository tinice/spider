# -*- coding: utf-8 -*-
import scrapy
import json
from redis_douban.items import doubanmovieItem, doubanactressItem
import re
from scrapy_redis.spiders import RedisSpider


class Movie250Spider(RedisSpider):
    name = 'doubanmovie'
    redis_key = 'myspider:start_urls'

    num = 0
    # allowed_domains = ["douban.com"]
    # tag_list = [
    #             '%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86',
    #             '%E6%9C%80%E6%96%B0',
    #             '%E7%83%AD%E9%97%A8',
    #             '%E5%8D%8E%E8%AF%AD',
    #             '%E6%AC%A7%E7%BE%8E',
    #             '%E9%9F%A9%E5%9B%BD',
    #             '%E6%97%A5%E6%9C%AC',
    #             '%E5%8A%A8%E4%BD%9C',
    #             '%E5%96%9C%E5%89%A7',
    #             '%E7%88%B1%E6%83%85',
    #             '%E5%8F%AF%E6%92%AD%E6%94%BE',
    #             '%E7%A7%91%E5%B9%BB',
    #             '%E5%86%B7%E9%97%A8%E4%BD%B3%E7%89%87',
    #             '%E6%82%AC%E7%96%91',
    #             '%E6%81%90%E6%80%96',
    #             '%E6%88%90%E9%95%BF'
    #             ]
    # start_urls = [
    #     "https://movie.douban.com/j/search_subjects?type=movie&tag={0}&sort=time&"\
    #     "page_limit=20&page_start={1}".format(tag, num * 20) for tag in tag_list for num in range(0, 23)
    #     ]

    #
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, meta={'dont_redirect': True,
    #                                         'handle_httpstatus_list': [302]}, callback=self.parse)

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(Movie250Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.log('response from {}'.format(response.url))
        try:
            item_list = json.loads(response.text)["subjects"]
        except Exception as e:
            self.log(e)
            self.log(response.text)
        if not item_list:
            self.log('NO DATA')
            self.log(response.url)
        else:
            for one in item_list:
                item = doubanmovieItem()
                item['name'] = one['title']
                item['score'] = one['rate']
                item['url'] = one['url']
                item['cover'] = one['cover']
                item['playable'] = one['playable']

                self.num += 1
                next_link = response.urljoin(item['url'] + '?from=subject-page')
                self.log("next_link {}".format(next_link))
                request=scrapy.Request(next_link, callback=self.parse_subject,dont_filter=True)
                request.meta['item'] = item
                request.meta['dont_redirect'] = True
                request.meta['handle_httpstatus_list'] = [302]
                yield request

    def parse_subject(self, response):
        self.log('response from {}'.format(response.url))
        try:
            item = response.meta['item']
        except KeyError:
            item = doubanmovieItem()
            item['name'] = response.css('#content > h1 > span:nth-child(1)::text').extract_first()
            item['score'] = response.css('#interest_sectl > div > div.rating_self.clearfix > strong::text').extract_first()
            item['url'] = response.url
            item['cover'] = response.css('#mainpic > a > img::attr(src)').extract_first()
            item['playable'] = 'unknown'
        info = response.css('#info')
        item['release_time'] = info.css('span[property=\'v:initialReleaseDate\']::attr(content)').extract()

        item['duration'] = info.css('span[property=\'v:runtime\']::text').extract_first()
        item['country'] = \
        re.findall('<span class="pl">制片国家/地区:</span>.+<br/>', response.text)[0].split('>')[-2].split('<')[0]
        try:
            item['language'] = \
            re.findall('<span class="pl">语言:</span>.+<br/>', response.text)[0].split('>')[-2].split('<')[0]
        except IndexError:
            item['language'] = 'unknown'
        item['tag'] = info.css('span[property=\'v:genre\']::text').extract()
        item['actress_list'] = info.css('a[rel=\'v:starring\']::attr(href)').extract()
        item['rate_num'] = response.css('span[property=\'v:votes\']::text').extract_first()
        yield item
        for url in item['actress_list']:
            next_link = response.urljoin('https://movie.douban.com'+url)
            self.log("next_link {}".format('https://movie.douban.com'+url))
            new_request = scrapy.Request(next_link, callback=self.parse_actress,dont_filter=True)
            new_request.meta['dont_redirect'] = True
            new_request.meta['handle_httpstatus_list'] = [302]
            yield new_request

    def parse_actress(self, response):
        self.log('response from {}'.format(response.url))

        item = doubanactressItem()
        item['url'] = response.url
        item['name'] = response.css('#content > h1::text').extract_first()
        info_list = response.css('#headline > div.info > ul > li')
        for one in info_list:
            if one.css('span::text').extract_first() == '性别':
                item['sex'] = ''.join(one.css('::text').extract()).replace('性别:', '').strip()
            if one.css('span::text').extract_first() == '出生日期':
                item['birthday'] = ''.join(one.css('::text').extract()).replace('出生日期:', '').strip()
            if one.css('span::text').extract_first() == '出生地':
                item['birthplace'] = ''.join(one.css('::text').extract()).replace('出生地:', '').strip()
        item['movie_list'] = []
        info_list = response.css('div.info')
        for one in info_list:
            tmp = one.css('a::attr(href)').extract_first()
            if tmp and 'subject' in tmp:
                item['movie_list'].append(tmp)
        yield item
        
        for url in item['movie_list']:
            next_link = url
            self.log("next_link {}".format(url))
            new_request = scrapy.Request(next_link, callback=self.parse_subject,dont_filter=True)
            new_request.meta['dont_redirect'] = True
            new_request.meta['handle_httpstatus_list'] = [302]
            yield new_request

        self.log('response from {} \n'.format(response.url))

    def closed(self, reason):
        self.log(reason)
        self.log(self.num)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
