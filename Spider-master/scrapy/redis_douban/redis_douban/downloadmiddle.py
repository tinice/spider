import logging as log
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost
from scrapy.core.downloader.handlers.http11 import TunnelError
import random
import string
import pymongo
import time
from redis_douban.agents import AGENTS_ALL


class CustomNormalMiddleware(object):
    IP_ERRORS = (ResponseNeverReceived, ConnectError, ConnectionLost, TunnelError, ValueError)
    SERVER_ERRORS = (TimeoutError, ConnectionRefusedError)

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://poluo:poluo123@ip:27017/proxy')
        self.db = self.client.proxy
        self.collection = self.db.proxy_list
        self.db_cycle_time = 60
        self.setting_list = []
        self.update_setting(None)
        self.request_count = 0

    def process_request(self, request, spider):
        log.debug('downloadmiddle process')
        if 'douban' in request.url:
            setting = random.choice(self.setting_list)
            # request.meta['proxy'] = 'https://{}:{}'.format(setting['proxy']['ip'], setting['proxy']['port'])
            request.cookies['bid'] = setting['cookies']
            request.headers['referer'] = 'https://movie.douban.com/'
            request.headers['User-Agent'] = setting['agent']
            request.dont_filter = True
            self.request_count += 1
        if self.request_count % 20 == 0:
            time.sleep(5)
            log.debug('sleep 5 seconds...')

    def process_response(self, request, response, spider):
        if response.status != 200:
            log.debug('{0}\n {1}'.format(response.headers, response.text))
            log.debug("response status not in 200 {}".format(response.status))
            time.sleep(60)
            log.debug('sleep 60 seconds...')
            tmp = {  # 'proxy': request.meta['proxy'],
                'cookies': request.cookies['bid'],
                'agent': request.headers['User-Agent']}
            self.update_setting(tmp)
            setting = random.choice(self.setting_list)
            return self.update_request(request, setting)
        else:
            return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.IP_ERRORS):
            log.debug("exception {}".format(exception))
            tmp = {  # 'proxy': request.meta['proxy'],
                'cookies': request.cookies['bid'],
                'agent': request.headers['User-Agent']}
            self.update_setting(tmp)
            setting = random.choice(self.setting_list)
            return self.update_request(request, setting)
        else:
            pass
        log.info('exception  {}'.format(exception))

    def update_request(self, request, setting):
        print(setting)
        new_request = request.copy()
        # new_request.meta['proxy'] = 'https://{}:{}'.format(setting['proxy']['ip'], setting['proxy']['port'])
        new_request.cookies['bid'] = setting['cookies']
        new_request.headers['referer'] = 'https://movie.douban.com/'
        new_request.headers['User-Agent'] = setting['agent']
        new_request.dont_filter = True
        return new_request


    def update_setting(self, setting):
        try:
            self.setting_list.remove(setting)
        except ValueError:
            pass

        while len(self.setting_list) == 0:
            result = self.collection.find().sort('speed', pymongo.ASCENDING)
            for one in result:
                setting = {
                    # 'proxy': one,
                    'cookies': "".join(random.sample(string.ascii_letters + string.digits, 11)),
                    'agent': random.choice(AGENTS_ALL)
                }
                self.setting_list.append(setting)
            if len(self.setting_list) == 0:
                log.info('update setting failed,sleep....')
                time.sleep(self.db_cycle_time)
            else:
                log.info('update setting succeed,get new setting {}.'.format(len(self.setting_list)))
