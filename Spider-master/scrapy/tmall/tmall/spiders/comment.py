# -*- coding: utf-8 -*-
import scrapy
import json
from tmall.items import TmallItem


class CommentSpider(scrapy.Spider):
    name = "comment"
    allowed_domains = ["tmall.com"]
    start_urls = ['https://www.tmall.com/']

    def parse(self, response):
        raw_data_str = response.css('#J_defaultData::text').extract_first()
        raw_data_json = json.loads(raw_data_str)
        tmp_category = raw_data_json['mockPage']['100']['categoryMainLines']
        category_dict = self.process_cat(tmp_category)
        # self.logger.debug(category_dict)
        for one in category_dict.values():
            if one:
                host = one.replace('//', '').split('/')[0]
                self.logger.info(one)
                if 'list' in host:
                    yield scrapy.Request(url='https:' + one, callback=self.parse_every_category,
                                         meta={'Host': 'list.tmall.com', 'headers': True})
                else:
                    yield scrapy.Request(url='https:' + one, callback=self.parse_category,
                                         meta={'Host': host, 'headers': True})
            break

    def parse_category(self, response):
        raw_data = response.css('#J_TmFushiNavCate > ul > li > ul.cate-bd.clearfix > li')
        if not raw_data:
            raw_data = response.css('div.slider-content > div.jia-left-nav > ul > li > a')
        if not raw_data:
            raw_data = response.css('ul.cate-nav > li > ul.cate-bd.clearfix > li > a')
        if not raw_data:
            raw_data = response.css('#J_MuiCategoryMenu > ul > li > a.cat-heigh-light')

        if not raw_data:
            self.logger.warning(response.url)

        for one in raw_data:
            link = one.css('::attr(href)').extract_first()
            self.logger.info('get sub category https:' + link)
            yield scrapy.Request(url='https:' + link, callback=self.parse_every_category,
                                 meta={'Host': 'list.tmall.com', 'headers': True})

    def parse_every_category(self, response):
        raw_data = response.css('#J_ItemList > div')
        for one in raw_data:
            name = one.css('div > p.productTitle > a::text').extract_first()
            url = one.css('div > p.productTitle > a::attr(href)').extract_first()
            price = one.css('div > p.productPrice > em::attr(title)').extract_first()
            shop_name = one.css('div > div.productShop > a::text').extract_first()
            shop_url = one.css('div > div.productShop > a::attr(href)').extract_first()
            yield TmallItem({'name': name, 'url': url, 'price': price, 'shop_name': shop_name, 'shop_url': shop_url})

        next_page = response.css(
            '#content > div.main > div.ui-page > div > b.ui-page-num > a.ui-page-next::attr(href)').extract_first()
        if next_page:
            next_page = 'https://list.tmall.com/search_product.htm' + next_page
            self.logger.info('next page {}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse_every_category,
                                 meta={'Host': 'list.tmall.com', 'headers': True})

    @staticmethod
    def process_cat(category):
        res = {}
        for one in category:
            if 'action1' in one and 'title1' in one:
                tmp = {one['title1']: one['action1']}
                if tmp:
                    res.update(tmp)
            if 'action2' in one and 'title2' in one:
                tmp = {one['title2']: one['action2']}
                if tmp:
                    res.update(tmp)
            if 'action3' in one and 'title3' in one:
                tmp = {one['title3']: one['action3']}
                if tmp:
                    res.update(tmp)
        return res


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
