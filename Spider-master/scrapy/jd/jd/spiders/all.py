# -*- coding: utf-8 -*-
import scrapy
import json
from jd.items import JdItem
from scrapy.exceptions import CloseSpider
import time


class AllSpider(scrapy.Spider):
    name = "all"
    start_urls = (
        'https://www.jd.com/',
    )
    count = 0
    start = time.time()

    def parse(self, response):
        yield scrapy.Request('https://dc.3.cn/category/get?callback=getCategoryCallback', callback=self.parse_content,
                             meta={'authority': 'dc.3.cn', 'method': 'GET',
                                   'path': '/category/get?callback=getCategoryCallback', 'scheme': 'https',
                                   'cookies': True})

    def parse_content(self, response):
        url_list = self.process_data(response)
        for url in url_list:
            if 'act' not in url:
                path = url.replace('https://list.jd.com', '')
                yield scrapy.Request(url=url, callback=self.parse_page,
                                     meta={'authority': 'list.jd.com', 'method': 'GET',
                                           'path': path,
                                           'scheme': 'https', 'cookies': True})

    def parse_page(self, response):
        item_list = response.css('#plist > ul > li > div')
        data = []
        tmp_count = 0
        check_chat = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='
        for one in item_list:
            tmp_count += 1
            my_items = JdItem()
            my_items['SkuId'] = one.css('::attr(data-sku)').extract_first()
            my_items['img'] = one.css('div.p-img > a::attr(href)').extract_first()
            my_items['name'] = one.css('div.p-name > a > em::text').extract_first()
            my_items['url'] = one.css('div.p-name > a::attr(href)').extract_first()
            try:
                tmp = one.css('div.p-icons.J-pro-icons > img::attr(data-tips)').extract_first()
                my_items['is_jd'] = True
            except Exception as e:
                self.logger.info(e)
                my_items['is_jd'] = False
            data.append(my_items)
            if tmp_count >= 30:
                check_chat = ','.join([check_chat, my_items['SkuId'] + '&callback=jQuery270940&_=1492343539522'])
                yield scrapy.Request(url=check_chat, callback=self.parse_one, meta={'cookies': False, 'data': data})
                check_chat = 'https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds='
                tmp_count = 0
                data = []
            else:
                if tmp_count == 1:
                    check_chat = ''.join([check_chat, my_items['SkuId']])
                else:
                    check_chat = ','.join([check_chat, my_items['SkuId']])

        next_page = response.css('#J_bottomPage > span.p-num > a.pn-next::attr(href)').extract_first()
        if next_page:
            self.logger.info('next {}'.format(next_page))
            url = ''.join(['https://list.jd.com', next_page])
            yield scrapy.Request(url=url, callback=self.parse_page,
                                 meta={'authority': 'list.jd.com', 'method': 'GET',
                                       'path': next_page,
                                       'scheme': 'https', 'cookies': True})

    def parse_one(self, response):
        data = response.meta.get('data')
        CommentCount = json.loads(response.text[13:-2])
        for i, j in zip(CommentCount['CommentsCount'], data):
            if str(i['SkuId']) == j['SkuId']:
                my_item = {**j, **i}
                yield self.process_item(my_item)
            else:
                self.logger.warning('SkuId not equal {} {}'.format(i, j))

    def process_item(self, item):
        del item['ProductId']  # 同SkuId
        del item['ShowCountStr']
        del item['ShowCount']
        del item['CommentCountStr']  # 评论总数字符型
        del item['GoodCountStr']  # 好评总数字符型
        del item['GoodCount']
        del item['GoodRateShow']
        del item['GoodRateStyle']
        del item['AfterCount']  # 追加评论
        del item['AfterCountStr']
        del item['GeneralCountStr']  # 中评
        del item['GeneralCount']
        del item['GeneralRateShow']
        del item['GeneralRateStyle']
        del item['PoorCountStr']  # 差评
        del item['PoorCount']
        del item['PoorRateShow']
        del item['PoorRateStyle']
        return item

    def process_data(self, response):
        data = []
        tmp = json.loads(response.text.replace('getCategoryCallback', '')[1:-1], encoding='GB2312')
        for content in tmp['data']:
            for content_2 in content['s']:
                for content_3 in content_2['s']:
                    for content_4 in content_3['s']:
                        data.append(content_4['n'].split('|')[0])
        url_list = []
        for one in data:
            if str.isdigit(one[0]):
                url = ''.join(['https://list.jd.com/list.html?cat=', one])
            else:
                url = ''.join(['https://', one])
            # self.logger.debug(url)
            url_list.append(url)
        return url_list

    # call this to close spider
    def close_spider(self, reason):
        raise CloseSpider(reason=reason)

    # do something before spider close
    def closed(self, reason):
        self.logger.info('last time {}s'.format(time.time() - self.start))
        self.logger.info(reason)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
