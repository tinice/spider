# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem
from spider_project.JS import GET_SIGN
from six.moves.urllib import parse
import re


class Basic_extractSpider(scrapy.Spider):
    """
    This spider is an example spider which show people how to write a spider in
    this project to work

    If you have no idea what variable ``name`` means here, please read
    https://doc.scrapy.org/en/latest/intro/tutorial.html

    If you have no idea what variable ``taskid`` and ``entry`` means here, please read
    http://scrapy-guru.readthedocs.io/en/latest/before_start.html
    taskid and entry only make sense in this project.

    """
    taskid = "list_extract_pagination"
    name = taskid
    entry = "content/list_basic/1"

    def start_requests(self):
        """
        In the scrapy doc there are two ways to tell scrapy where to begin to
        crawl from.  One is start_requests, the other is start_urls which is
        shortcut to the start_requestt.

        Based on my experience, it is better to use start_requests instead of
        start_urls bacause in this methods you can know how the request object
        are created and how request is yield. You should keep it simple and
        try not to use some magic or it might confuse you.

        In this project, you have no need to change code in this method, just
        modify code in parse_entry_page

        If you fully understatnd how scrapy work, then you are free to choose
        between start_requests and start_urls.
        """
        prefix = self.settings["WEB_APP_PREFIX"]
        result = parse.urlparse(prefix)
        base_url = parse.urlunparse(
            (result.scheme, result.netloc, "", "", "", "")
        )
        # Generate start url from config and self.entry, when you paste the code
        # to another spider you can just change self.entry and self.taskid
        url = parse.urljoin(base_url, self.entry)
        request = Request(url=url, callback=self.parse_entry_page)
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        request.headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = '115.28.36.253:8000'
        request.headers['DNT'] = 1
        yield request

    def parse_entry_page(self, response):
        """
        This method is a callback, when scrapy got response from web server, then
        this method will be called to process the response.

        If you have no idea what yield keyword in python mean, please read
        http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
        """
        # we create a item here, fill the data, and yield it
        product_list = response.css('body > div > div > div > table > tbody > tr > td:nth-child(1) > a')
        for one in product_list:
            url = one.css('::attr(href)').extract_first()
            sku = url.split('/')[-1]
            title = one.css('::text').extract_first()
            yield scrapy.Request(url='http://115.28.36.253:8000'+url, meta={'sku': sku, 'title': title}, callback=self.parse_one)
        if product_list:
            index = response.url.split('/')[-1]
            yield scrapy.Request(url='http://115.28.36.253:8000/static/js/lib/jquery.simplePagination.js',
                                 meta={'index': int(index)}, callback=self.next,dont_filter=True)

    def parse_one(self, response):
        item = SpiderProjectItem()
        item['taskid'] = self.taskid
        tmp = {}
        tmp['sku'] = response.meta['sku']
        tmp['title'] = [response.meta['title']]
        tmp['price'] = [response.css(
            'body > div > div > div.item-container > div > div.col-md-7 > div.product-price::text').extract_first()]
        item["data"] = tmp
        yield item

    def next(self, response):
        if 'page-link' in response.text:
            index = response.meta['index'] + 1
            url = 'http://115.28.36.253:8000/content/list_basic/' + str(index)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_entry_page)

    if __name__ == '__main__':
        from scrapy.cmdline import execute

        execute()
