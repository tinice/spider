# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from reddit.items import UserItem


class UserSpider(scrapy.Spider):
    name = "user"
    allowed_domains = ["reddit.com"]
    start_urls = ['https://www.reddit.com/subreddits/']
    count = 0

    def parse(self, response):
        res = response.css('#siteTable > div > div > p.titlerow > a::attr(href)').extract()
        for one in res:
            path = one.replace('https://www.reddit.com', '')
            yield Request(url=one, callback=self.parse_tag, meta={'cookies': True, 'path': path})
        next_page = response.css(
            '#siteTable > div.nav-buttons > span > span.next-button > a::attr(href)').extract_first()
        self.count += 1
        if next_page and self.count < 10:
            path = next_page.replace('https://www.reddit.com', '')
            yield Request(url=next_page, callback=self.parse, meta={'cookies': True, 'path': path})
        else:
            self.logger.info('count = {}'.format(self.count))
            self.logger.info('NO next page in parse')

    def parse_tag(self, response):
        res = LinkExtractor(allow=('.*/user/.*'), allow_domains='www.reddit.com').extract_links(response)
        for one in res:
            if one.text != 'Click here!':
                path = one.url.replace('https://www.reddit.com', '')
                yield Request(url=one.url, callback=self.parse_user, meta={'cookies': True, 'path': path})

        res = LinkExtractor(allow=('.*/comments/.*'), allow_domains='www.reddit.com').extract_links(response)
        for one in res:
            path = one.url.replace('https://www.reddit.com', '')
            yield Request(url=one.url, callback=self.parse_comment, meta={'cookies': True, 'path': path})

        next_page = response.css(
            '#siteTable > div.nav-buttons > span > span.next-button > a::attr(href)').extract_first()
        if next_page:
            path = next_page.replace('https://www.reddit.com', '')
            yield Request(url=next_page, callback=self.parse_tag, meta={'cookies': True, 'path': path})
        else:
            self.logger.info('No next page in parse_tag')

    def parse_comment(self, response):
        # Do not show all comment
        res = LinkExtractor(allow=('.*/user/.*'), allow_domains='www.reddit.com').extract_links(response)
        for one in res:
            path = one.url.replace('https://www.reddit.com', '')
            yield Request(url=one.url, callback=self.parse_user, meta={'cookies': True, 'path': path})

    def parse_user(self, response):
        site_table = response.css('#siteTable > div')
        user = response.url.replace('https://www.reddit.com/user/', '')
        res = []
        for one in site_table:
            data_type = one.css('::attr(data-type)').extract_first()
            if data_type == 'link':
                url = one.css('::attr(data-url)').extract_first()
                title = one.css('div.entry.unvoted > p.title > a::text').extract_first()
                time = one.css('div.entry.unvoted > p.tagline > time::attr(datetime)').extract_first()
                num = one.css('div.midcol.unvoted > div.score.unvoted::text').extract_first()
                tag = one.css('div.entry.unvoted > p.tagline > a::attr(href)').extract()[-1]
                data = {'type': data_type, 'url': url, 'title': title, 'num': num, 'tag': tag, 'time': time}
                # self.logger.info('Got data {}'.format(data))
            elif data_type == 'comment':
                tmp = one.css('p.parent > a.title')
                url = tmp.css('::attr(href)').extract_first()
                title = tmp.css('::text').extract_first()
                tag = one.css('p.parent > a.subreddit.hover::attr(href)').extract()[-1]
                time = one.css('div.entry.unvoted > p > time::attr(datetime)').extract_first()
                comment = one.css('div.usertext-body.may-blank-within.md-container > div.md > p::text').extract()
                num = one.css('div.midcol.unvoted > div:nth-child(1)::text').extract_first()
                data = {'type': data_type, 'url': url, 'title': title, 'num': num, 'tag': tag, 'time': time,
                        'comment': comment}
                # self.logger.info('Got data {}'.format(data))
            else:
                pass

            res.append(data)
        yield UserItem({'user': user, 'info': res})

    def closed(self, reason):
        pass


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
