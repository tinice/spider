# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from quora.items import QuoraItem


class UserSpider(scrapy.Spider):
    name = "user"
    allowed_domains = ["quora.com"]
    start_urls = (
        'https://www.quora.com/webnode2/server_call_POST',
    )
    frmdata = {}
    frmdata['json'] = '{"args":[],"kwargs":{"email":"email","password":"passwd"}}'
    frmdata['formkey'] = '75ec5150317eefe0dae46fc9f101a5da'
    frmdata['postkey'] = '38b460e8664939fb1c080a6244e14193'
    frmdata['window_id'] = 'dep3302-2238714638416261581'
    frmdata['referring_controller'] = 'index'
    frmdata['referring_action'] = 'index'
    frmdata['__vcon_json'] = '["Vn03YsuKFZvHV9"]'
    frmdata['__vcon_method'] = 'do_login'
    frmdata['__e2e_action_id'] = 'eofxmib3zd'
    frmdata['js_init'] = '{}'
    frmdata['__metadata'] = '{}'
    cookies = {'m-b': 'pGLDg-FVmqrI6CF2993g9g\075\075', 'm-s': 'w99B2D2muwOFbchfKrmDbw\075\075',
               'm-css_v': '35c555df5890b2f8',
               'm-login': '0', 'm-early_v': '0f20c735abd3a97d', 'm-tz': '-480', 'm-wf-loaded': 'q-icons-q_serif',
               '_ga': 'GA1.2.420550872.1490615030'}

    passed_list = ['/profile/Poluo-Tomas']

    def start_requests(self):
        for one in self.start_urls:
            yield FormRequest(one, cookies=self.cookies, formdata=self.frmdata, callback=self.parse, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': 'https://www.quora.com/'})

    def parse(self, response):
        self.cookies['m-login'] = '1'
        url = 'https://www.quora.com/'
        yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_page)

    def parse_page(self, response):
        # get original user from my home page
        user_list = response.css('a.user::attr(href)').extract()
        return self.process_usrlist(user_list)

    def parse_followers(self, response):
        user_list = response.css('a.user::attr(href)').extract()
        return self.process_usrlist(user_list)

    def process_usrlist(self, user_list):
        for one in user_list:
            if str.isdigit(one[-1]):
                num = one.split('-')[-1]
                one = one.replace('-' + str(num), '')
            else:
                num = 0
            self.logger.info('Name {} Num {}'.format(one, num))
            yield QuoraItem({'Name': one, 'Num': num})
            url = 'https://www.quora.com' + one + '/followers'
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_followers)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
