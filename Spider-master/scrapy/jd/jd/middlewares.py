import logging as log
from jd.agents import AGENTS
import random


class CustomNormalMiddleware(object):
    def __init__(self):
        self.cookies = {'__jdv': '122270672|direct|-|none|-|1492518342585', 'ipLoc-djd': '1-72-4137-0', 'areaId': '1',
                         'listck': '6540956f5e73b2a6cfc055a9a6ec1055',
                         '__jda': '122270672.1492518342584482870352.1492518343.1492518343.1492518343.1',
                         '__jdb': '122270672.4.1492518342584482870352|1.1492518343', '__jdc': '122270672',
                         '__jdu': '1492518342584482870352',
                         '3AB9D23F7A4B3C9B': 'WDHQLJX6VWBVJJXVREUHFRGVBG4GVXSK4IDXNH7ESUNO3F2JPCKO46I6472NNOFFTOYQZEU265HMUZKNXDW635METQ'}

    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(AGENTS)
        request.headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['referer'] = 'https://www.jd.com/'
        request.headers['cache-control'] = 'max-age=0'
        try:
            cookies_enable = request.meta.get('cookies')
        except Exception as e:
            log.info(e)
            cookies_enable = True
        if cookies_enable:
            try:
                self.cookies[':authority'] = request.meta.get('authority')
                self.cookies[':method'] = request.meta.get('method')
                self.cookies[':path'] = request.meta.get('path')
                self.cookies[':scheme'] = request.meta.get('scheme')
            except Exception as e:
                log.info(e)
                self.cookies[':authority'] = 'www.jd.com'
                self.cookies[':method'] = 'GET'
                self.cookies[':path'] = '/'
                self.cookies[':scheme'] = 'https'
            request.cookies = self.cookies
