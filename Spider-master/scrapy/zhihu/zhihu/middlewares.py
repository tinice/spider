import logging as logger
import random
import requests
import os
import time


class CrawlMiddleware(object):
    def __init__(self):
        self.setting = []
        self.count = 0
        self.change_ip()
        res = self.get_new_cookies()
        auth = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
        self.setting.append({'cookies': res, 'auth': auth, 'xudid': None})

    def process_request(self, request, spider):
        setting = random.choice(self.setting)
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        request.headers['accept'] = 'application/json, text/plain, */*'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = 'www.zhihu.com'
        request.headers['Referer'] = 'https://www.zhihu.com/'
        request.headers['If-Modified-Since'] = 'Sun, 04 Jun 2017 02:44:58 GMT'
        request.headers['If-None-Match'] = 'W/"0a76c6fbe821b42dc7046ecf3e05458b63d12dd1"'
        request.cookies = setting['cookies']
        # logger.info('request cookies')
        # logger.info(request.cookies)
        Referfer = request.meta.get('referer')
        if Referfer:
            request.headers['Referer'] = Referfer
            request.headers['x-api-version'] = '3.0.40'
            request.headers['x-udid'] = setting['xudid']
            request.headers['authorization'] = setting['auth']

    def get_new_cookies(self):
        s = requests.get('https://www.zhihu.com/people/nan-qian-42/activities')
        data = s.headers['Set-Cookie']
        res = {}
        if 'aliyungf_tc' in data:
            tmp = data.split(';')[0]
            if tmp.split('=')[0] == 'aliyungf_tc':
                res['aliyungf_tc'] = tmp.split('=')[1]

        if 'acw_tc' in data:
            tmp = data.split(';')[2]
            if tmp[tmp.index(',') + 2:tmp.index('=')] == 'acw_tc':
                res['acw_tc'] = tmp[tmp.index('=') + 1:]
        return res

    def process_response(self, request, response, spider):
        self.count += 1
        if 'unhuman' in response.url:
            logger.info('response not right')
            self.change_ip()
            self.get_new_cookies()
            self.process_request(request, spider)
            return response
        else:
            return response

        if self.count > 3000:
            self.change_ip()
            self.get_new_cookies()
            self.count = 0

    @staticmethod
    def change_ip():
        cmd_str = "adsl-stop"
        os.system(cmd_str)
        time.sleep(1)
        cmd_str = "adsl-start"
        os.system(cmd_str)
        time.sleep(1)
