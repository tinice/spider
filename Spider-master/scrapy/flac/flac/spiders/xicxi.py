# -*- coding: utf-8 -*-
import scrapy
import json


class XicxiSpider(scrapy.Spider):
    name = "xicxi"
    link_list = []
    passed_list=[]
    base_url = 'http://www.xicxi.com'
    allowed_domains = ["xicxi.com"]
    start_urls = (
        'http://www.xicxi.com/',
    )
    data = []
    count = 0
    threshold = 5000

    # parse_links
    def parse(self, response):
        link_list = response.css('body > div.head > div > ul > li')
        self.log(len(link_list))
        for link in link_list:
            try:
                tmp = link.css('a::attr(href)').extract_first()
                self.link_list.append(tmp)
                self.log(tmp)
            except Exception as e:
                self.log(e)
                pass
        for link in self.link_list:
            if 'ape' in link:
                yield scrapy.Request(response.urljoin(self.base_url + link), callback=self.process_ape)
            elif 'flac' in link:
                yield scrapy.Request(response.urljoin(self.base_url + link), callback=self.process_ape)
            elif 'wav' in link:
                yield scrapy.Request(response.urljoin(self.base_url + link), callback=self.process_ape)
            elif 'gs' in link:
                yield scrapy.Request(response.urljoin(self.base_url + link), callback=self.process_gs)
            elif 'zhuanji' in link:
                yield scrapy.Request(response.urljoin(self.base_url + link), callback=self.process_ape)

    def process_ape(self, response):
        self.log('process {}'.format(response.url))
        element_list = response.css('#main > div.left_content > div.pleft > div.listbox > ul > li')
        for element in element_list:
            name = element.css('a.l_gm::text').extract_first().split('-')
            song_name = name[0]
            singer_name = name[1]
            data = {
                'href': element.css('a.l_gm::attr(href)').extract_first(),
                'song_name': song_name,
                'singer_name': singer_name,
                'size': element.css('span.l_size::text').extract_first(),
                'album': element.css('a.l_zhuanji::text').extract_first(),
                'format': element.css('a.l_leixing::text').extract_first()
            }
            self.data_join(data)

        next_page = response.css('#main > div.left_content > div.pleft > div.dede_pages > ul > '
                                 'li:nth-last-child(2) > a::attr(href)').extract_first()
        if next_page:

            if 'ape' in response.url:
                yield scrapy.Request(response.urljoin('http://www.xicxi.com/ape/' + next_page), callback=self.process_ape)
            elif 'flac' in response.url:
                yield scrapy.Request(response.urljoin('http://www.xicxi.com/flac/' + next_page), callback=self.process_ape)
            elif 'wav' in response.url:
                yield scrapy.Request(response.urljoin('http://www.xicxi.com/wav/' + next_page), callback=self.process_ape)
            elif 'zhuanji' in response.url:
                yield scrapy.Request(response.urljoin('http://www.xicxi.com/zhuanji/' + next_page),
                                     callback=self.process_ape)
            elif 'gs' in response.url:
                next_page = response.url.split('/')[4] + '/' + next_page
                yield scrapy.Request(response.urljoin('http://www.xicxi.com/gs/'+next_page),
                                     callback=self.process_ape)

    def process_gs(self, response):
        singer_list = []
        tmp_list = response.css('body > div.module_1 > div > div.all_singers > li')
        for one in tmp_list:
            singer = {
                'href': one.css('a::attr(href)').extract_first(),
                'name': one.css('a::text').extract_first()
            }
            singer_list.append(singer)
        for one in singer_list:
            yield scrapy.Request(response.urljoin('http://www.xicxi.com') + one['href'], callback=self.process_ape)

    def data_join(self, data):
        if len(self.data) > self.threshold:
            with open('data_{}.json'.format(self.count), 'w') as fobj:
                json.dump(self.data, fobj)
            self.data = []
            self.count += 1
        if data['href'] not in self.passed_list:
            self.passed_list.append(data['href'])
            self.data.append(data)

    def closed(self, reason):
        with open('data_{}.json'.format(self.count), 'w') as fobj:
            json.dump(self.data, fobj)
        self.log('crawled data num:{}'.format(self.count * self.threshold + len(self.data)))
        self.log(reason)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
