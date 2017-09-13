# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http.request import Request
from spider_project.items import SpiderProjectItem
from spider_project.JS import GET_SIGN
from six.moves.urllib import parse


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
    taskid = "ajax_sign"
    name = taskid
    entry = "content/detail_sign"

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
        print(url)
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
        # request.cookies['token'] = '4TO4N49X81'

        yield request

    def parse_entry_page(self, response):
        """
        This method is a callback, when scrapy got response from web server, then
        this method will be called to process the response.

        If you have no idea what yield keyword in python mean, please read
        http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
        """
        print(response.headers)
        token = str(response.headers['Set-Cookie'])
        token = str(token.split(';')[0][2:])
        # we create a item here, fill the data, and yield it
        tmp = {}
        tmp['description'] = response.css('#service-one > section > li::text').extract()
        token = token[6:]
        sign = GET_SIGN(token)
        request = Request(url='http://115.28.36.253:8000/content/ajaxdetail_sign?sign=' + sign, callback=self.parse_ajax)
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        request.headers[
            'Accept'] = '*/*'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = '115.28.36.253:8000'
        request.headers['DNT'] = 1
        request.headers['Referer'] = 'http://115.28.36.253:8000/content/detail_sign'
        request.headers['X-Requested-With']  ='XMLHttpRequest'
        request.meta['data'] = tmp
        yield request

    def parse_ajax(self, response):
        item = SpiderProjectItem()
        item["taskid"] = self.taskid
        tmp = json.loads(response.text)
        tmp['description'] = response.meta['data']['description']
        item["data"] = tmp
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
