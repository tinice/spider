# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
import json
from Netease.items import NeteaseItem
from scrapy_redis.spiders import RedisSpider


class MusicSpider(RedisSpider):
    name = "music"
    allowed_domains = ["music.163.com"]
    redis_key = 'music:start_urls'
    # start_urls = (
    #     'http://music.163.com/discover/playlist',
    # )

    # first get tag links
    def parse(self, response):
        tag_list = []
        raw_data = response.css("a.s-fc1 ")
        for tag in raw_data:
            tag_offset = tag.css('::attr(href)').extract_first()
            tag_list.append(tag_offset)
            tag_name = tag.css('::text').extract_first()
            # self.logger.debug('{} {}'.format(tag_offset, tag_name))

        playlist_base_url = 'http://music.163.com'
        for one in tag_list:
            yield Request(url=playlist_base_url + one, callback=self.parse_tag)

    # second farse tags
    def parse_tag(self, response):
        if 'hot' in response.url:
            order_by_new_url = response.url.replace('hot', 'new')
            # self.logger.debug(order_by_new_url)
            yield Request(url=order_by_new_url, callback=self.parse_tag)

        raw_data = response.css('#m-pl-container > li')
        playlist_urls = []
        for one in raw_data:
            # m-pl-container > li:nth-child(1) > div
            url = one.css('div > a::attr(href)').extract_first()
            title = one.css('div > a::attr(title)').extract_first()
            img = one.css('div > img::attr(src)').extract_first()
            # m-pl-container > li:nth-child(1) > div > div > span.nb
            play_num = one.css('div > div > span.nb::text').extract_first()
            creater_url = one.css('p:nth-last-child(1) > a::attr(href)').extract_first()
            creater_name = one.css('p:nth-last-child(1) > a::text').extract_first()
            playlist_urls.append(url)
            # self.logger.debug('{} {} {} {} {} {}'.format(url, title, img, play_num, creater_name, creater_url))
        base_url = 'http://music.163.com'
        for one in playlist_urls:
            yield Request(url=base_url + one, meta={'url': url}, callback=self.parse_playlist)
        if 'new' not in response.url:
            next_page_url = response.css('#m-pl-pager > div > a.zbtn.znxt::attr(href)').extract_first()

            if 'playlist' in next_page_url:
                self.logger.info('next page {}'.format(next_page_url))
                yield Request(url=base_url + next_page_url, callback=self.parse_tag)

    # Third steps,parse playlist
    def parse_playlist(self, response):
        self.logger.info(response.url)
        # m-playlist > div.g-sd4 > div > ul
        more_playlist = response.css('ul.m-rctlist.f-cb > li')
        for one in more_playlist:
            link = one.css('div.cver.u-cover.u-cover-3 > a::attr(href)').extract_first()
            yield Request('http://music.163.com'+link,callback=self.parse_playlist)

        text = re.search('<textarea style="display:none;">.*</textarea>', response.text)
        if text:
            text = re.sub('</textarea>', '', text.group())
            text = re.sub('<textarea style="display:none;">', '', text)
            raw_data = json.loads(text)
            song_list = []
            for one in raw_data:
                # self.logger.debug(one)
                song = {
                    'name': one['name'],
                    'id': one['id'],
                    'duration': one['duration'],
                    'artists': '',
                    'ablum_name': one['album']['name'],
                    'artists_id': '',
                    'ablum_id': one['album']['id']
                }
                for tmp in one['artists']:
                    song['artists'] += ' ' + tmp['name']
                    song['artists_id'] += ' ' + str(tmp['id'])
                    # self.logger.debug(song)
                song_list.append(song)
            yield NeteaseItem({'url': response.url, 'song_list': song_list})


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
