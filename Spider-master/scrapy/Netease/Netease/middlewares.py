import logging as logger
import random
import subprocess
import time
from Netease.agents import AGENTS_ALL


class CrawlMiddleware(object):
    def __init__(self):
        self.request_count = 0
        self.change_ip()
        # self.cookie = self.get_new_cookies()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.agent
        request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate,sdch'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        # request.headers['Host'] = 'music.163.com/'
        request.headers['Referer'] = 'http://music.163.com/'
        request.headers['Upgrade-Insecure-Requests'] = '1'
        request.headers['DNT'] = '1'
        self.request_count += 1
        if self.request_count > 15000:
            logger.info('count more than 15000,need change ip')
            self.change_ip()

    def process_response(self, request, response, spider):
        if response.status != 200:
            if self.request_count < 5:
                return request
            logger.info('response status not 200,need change ip {}'.format(response.status))
            self.change_ip()
            return request
        else:
            return response

    def change_ip(self):
        self.agent = random.choice(AGENTS_ALL)
        self.request_count = 0
        status, res = subprocess.getstatusoutput('adsl-stop')
        if status == 0:
            logger.debug('adsl stop success')
        else:
            logger.warning('adsl stop failed')
        time.sleep(0.5)
        status, res = subprocess.getstatusoutput('adsl-start')
        if status == 0:
            logger.debug('adsl start success')
        else:
            logger.warning('adsl start failed')
