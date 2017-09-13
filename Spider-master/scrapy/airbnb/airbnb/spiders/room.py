# -*- coding: utf-8 -*-
import scrapy
from furl import furl
import json
import re
from airbnb.items import AirbnbItem, UserItem
import time


class RoomSpider(scrapy.Spider):
    name = "room"
    start_urls = (
        'https://zh.airbnb.com/s/Shanghai--China?cdn_cn=1&page=1&s_tag=5YFxd8A3&allow_override%5B%5D=',
        'https://zh.airbnb.com/s/Kyoto--Japan?guests=1&cdn_cn=1&page=1&s_tag=6UdMM010&allow_override%5B%5D=',
        'https://zh.airbnb.com/s/London--United-Kingdom?guests=1&cdn_cn=1&page=1&s_tag=lnzfSB2q&allow_override%5B%5D=',
        'https://zh.airbnb.com/s/Bangkok-Thailand?cdn_cn=1&page=1&s_tag=L3oOdNXc&allow_override%5B%5D=',
    )
    start = time.time()

    def parse(self, response):
        room_list = response.css('div.row_2h22gn')
        for one in room_list:
            url = one.css('div.infoContainer_v72lrv > a::attr(href)').extract_first()
            yield scrapy.Request(url='https://zh.airbnb.com' + url, callback=self.parse_room_first)

    def parse_room_first(self, response):
        id = re.findall(r'\d{3,10}', response.url)[0]
        name = response.css('#listing_name::text').extract_first()
        # equipment = response.css(
        #     'div.row.row-condensed.text-muted.text-center.hide-sm > div > div.col-sm-3.icon--small-margin > span.text-small::text').extract()
        # img = response.css('.cover-img::attr(style)').extract_first().replace('ackground-image:url', '')[1:-1]
        # description = response.css('div.simple-format-container > p > span::text').extract()
        # comment_num = response.css('div.col-md-8.review-header > div > h4 > span > span::text').extract_first()
        owner = response.css(
            'div.host-info.pull-left > div > span > a.link-reset::attr(href)').extract_first().split('：')[-1]
        owner_id = response.css(
            'div.host-info.pull-left > div > span > a.link-reset > span::text').extract_first()
        f = furl(response.url)
        f.path.add('personalization.json')
        try:
            del f.args['location']
        except KeyError:
            pass
        f.args.addlist('review_ids[]',
                       ['144474925', '141633062', '140450604', '139913674', '138701100', '138102086', '137690239'])
        url = f.url
        path = str(f.path) + str(f.query)
        return scrapy.FormRequest(url=url, callback=self.parse_room_second,
                                  meta={'room_id': id, 'name': name, 'owner': owner, 'owner_id': owner_id,
                                        'parse': True})

    def parse_room_second(self, response):
        try:
            flag = response.meta.get('parse')
        except Exception as e:
            self.logger.info(e)
        if flag:
            self.logger.info('From First {}'.format(response.url))
            data = json.loads(response.text)
            price = data['nightly_price']  # not exactly
            name = response.meta.get('name')
            owner = response.meta.get('owner')
            owner_id = response.meta.get('owner_id')
            room_id = response.meta.get('id')
            yield AirbnbItem({'room_id': room_id, 'name': name, 'owner': owner, 'owner_id': owner_id,
                              'price': price})
            room_id = re.findall(r'\d{3,10}', response.url)[0]
        else:

            self.logger.info('From similar {}'.format(response.url))
            room_id = response.url.split('/')[-1]

        guest_list = response.css('div.show-inline-block > div:nth-child(2) > div > div.name > a')
        for one in guest_list:
            name = one.css('span::text').extract_first()
            guest_id = one.css('::attr(href)').extract_first()
            yield UserItem({'name': name, 'user_id': guest_id})

        self.logger.info('id = {}'.format(room_id))
        f = furl('https://zh.airbnb.com/api/v2/similar_listings?')
        arg = {'key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20', 'currency': 'CNY', 'locale': 'zh',
               '_format': 'for_listing_card', 'filter_instant_book': 'false', 'listing_id': str(room_id)}
        f.add(args=arg)
        url = f.url
        path = f.query
        yield scrapy.FormRequest(url=url, callback=self.parse_similar)

    def parse_similar(self, response):
        data = json.loads(response.text)
        for one in data['similar_listings']:
            room_id = one['listing']['id']
            name = one['listing']['name']
            owner = one['listing']['primary_host']['first_name']
            owner_id = one['listing']['primary_host']['id']
            price = one['pricing_quote']['rate']['amount_formatted']
            yield AirbnbItem({'room_id': room_id, 'name': name, 'owner': owner, 'owner_id': owner_id,
                              'price': price})
            yield scrapy.Request(url='https://zh.airbnb.com/rooms/' + str(room_id), meta={'parse': False},
                                 callback=self.parse_room_second)

    def closed(self, reason):
        self.logger.info(reason)
        self.logger.info('time = {}'.format(time.time() - self.start))


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
