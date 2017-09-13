# -*- coding: utf-8 -*-
import scrapy
from taobao.items import GoodsItem
from taobao.settings import SPIDER_CONTENTS


class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["taobao.com"]
    count = 0

    def start_requests(self):
        selector = 'div.search-combobox > div.search-combobox-input-wrap > input'
        for one in SPIDER_CONTENTS:
            content = one
            self.logger.info(content)
            yield scrapy.Request(url='https://www.taobao.com/', callback=self.parse_content, dont_filter=True,
                                 meta={'send_keyword': 1, 'content': content, 'selector': selector, 'selenium': 1})

    def parse_content(self, response):
        my_goods = GoodsItem()
        goods_list = response.css('#mainsrp-itemlist > div > div > div:nth-child(1) > div')
        if not goods_list:
            self.logger.info("ERROR")
        for goods in goods_list:
            name = goods.css('div.row.row-2.title > a').extract_first()
            try:
                my_goods['name'] = name[name.find('</span>') + 7:name.find('</a>')].strip(). \
                    replace('<span class="H">', '').replace('</span>', '')
            except AttributeError:
                self.logger.error('goods name error!')
                my_goods['name'] = '提取出错'
            my_goods['link'] = goods.css('div.row.row-2.title > a::attr(href)').extract_first()
            my_goods['image'] = goods.css('div > div > div.pic > a > img::attr(src)').extract_first()
            my_goods['price'] = goods.css(
                'div.row.row-1.g-clearfix > div.price.g_price.g_price-highlight > strong::text').extract_first()
            my_goods['sales'] = goods.css('div.row.row-1.g-clearfix > div.deal-cnt::text').extract_first()
            my_goods['shop_name'] = goods.css(
                'div.row.row-3.g-clearfix > div.shop > a > span:nth-child(2)::text').extract_first()
            my_goods['shop_url'] = goods.css('div.row.row-3.g-clearfix > div.shop > a::attr(href)').extract_first()
            my_goods['shop_location'] = goods.css('div.row.row-3.g-clearfix > div.location::text').extract_first()
            yield my_goods
        next_page = '#mainsrp-pager > div > div > div > ul > li.item.next > a'
        if next_page:
            self.count += 1
            self.logger.info('count {}, url = {}'.format(self.count, response.url))
            yield scrapy.Request(url=response.url, callback=self.parse_content,
                                 meta={'click': 1, 'selector': next_page, 'selenium': 1})
        else:
            self.logger.info('no next page {}'.format(self.count))


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
