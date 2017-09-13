from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost
from scrapy.core.downloader.handlers.http11 import TunnelError
import re
from scrapy.exceptions import IgnoreRequest
import time
import random
import logging as log
import requests
import json
import base64
import os


class CustomNormalMiddleware(object):
    IP_ERRORS = (ResponseNeverReceived, ConnectError, ConnectionLost,
                 TunnelError, TimeoutError, ConnectionRefusedError)

    def __init__(self):
        # for abuyun
        # 代理服务器
        self.proxyHost = "proxy.abuyun.com"
        self.proxyPort = "9010"
        # 代理隧道验证信息
        self.proxyUser = "H2W595AM4Y5H902P"
        self.proxyPass = "ADDEFEB88B2E42D5"
        self.proxyAuth = "Basic " + base64.urlsafe_b64encode(
            bytes((self.proxyUser + ":" + self.proxyPass), "ascii")).decode("utf8")

        # for abuyun
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }
        self.proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }

        self.cookies = None
        self.agent = None
        self.request_count = 0
        self.used_set = []
        self.update_setting()

    def process_request(self, request, spider):
        self.request_count += 1
        if self.request_count > 4000000:
            self.request_count = 0
            log.info('request more than 400,update setting')
            self.update_setting()
        if 'signin' in request.url:
            log.info('need sign in,try sleep 2s...')
            time.sleep(2)
        if 'dp' in request.url:
            tmp = re.compile(r'/dp/.{10}/').findall(request.url)
            if tmp not in self.used_set:
                flag = True
                self.used_set.append(tmp)
            else:
                flag = False
        else:
            flag = True

        if flag:
            # for abuyun
            # request.meta["proxy"] = "http://proxy.abuyun.com:9010"
            # request.headers["Proxy-Authorization"] = self.proxyAuth
            request.headers['User-Agent'] = self.agent
            request.headers[
                'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
            request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
            request.headers['Connection'] = 'keep-alive'
            request.headers['Host'] = 'www.amazon.cn'
            request.cookies = self.cookies
        else:
            raise IgnoreRequest

    def update_setting(self):
        while True:
            # 　abunyu do not need get proxy
            self.change_proxy()
            self.get_new_cookie()
            if self.cookies != {}:
                break
            else:
                log.info('cookies in empty,try again')

    def process_response(self, request, response, spider):
        if 'book' in response.url:
            name = response.css(
                '#title > span:nth-child(1)::text').extract_first()
        else:
            name = 1
        if '自动程序' in response.text or not name:
            log.info('robot check happened,update setting')
            self.update_setting()
        return response

    def change_proxy(self):
        # r = requests.get('http://proxy.abuyun.com/switch-ip',
        #                  timeout=5, proxies=self.proxies)
        # log.info('new proxy')
        # log.info(r.text)
        cmd_str = "pppoe-stop"
        os.system(cmd_str)
        time.sleep(2)
        cmd_str = "pppoe-start"
        os.system(cmd_str)
        time.sleep(5)

    def get_new_cookie(self):
        from amazon.agents import AGENTS
        self.agent = random.choice(AGENTS)
        headers = {'user-agent': self.agent}
        flag = 1
        count = 0
        log.info(headers)
        while flag:
            try:
                # for abuyun
                r = requests.get('https://www.amazon.cn', headers=headers, timeout=5,)# proxies=self.proxies)
            except Exception as e:
                log.info(e)
                count += 1
                time.sleep(2)
                if count > 3:
                    self.change_proxy()
            else:
                flag = 0
            finally:
                log.info('count {}'.format(count))
        cookies = r.headers['Set-Cookie'].split(';')
        result = {}
        for one in cookies:
            if 'session-id-time' in one:
                tmp = one.split(',')[-1].split('=')[-1]
                if tmp != '-':
                    result['session-id-time'] = tmp
            elif 'session-id' in one and 'time' not in one:
                tmp = one.split(',')[-1].split('=')[-1]
                if tmp != '-':
                    result['session-id'] = tmp
            elif 'x-wl-uid' in one:
                tmp = one.split(',')[-1].split('=')[1]
                if tmp != '-':
                    result['x-wl-uid'] = tmp
            elif 'x-acbcn' in one:
                tmp = one.split(',')[-1].split('=')[1]
                if tmp != '-':
                    result['x-acbcn'] = tmp
            elif 'csm-hit' in one:
                tmp = one.split(',')[-1].split('=')[1]
                if tmp != '-':
                    result['csm-hit'] = tmp
            elif 'ubid-acbcn' in one:
                tmp = one.split(',')[-1].split('=')[1]
                if tmp != '-':
                    result['ubid-acbcn'] = tmp
        log.info('new cookies {}'.format(result))
        self.cookies = result
        with open('cookies_dump.json', 'a') as fobj:
            line = json.dumps(self.cookies) + '\n'
            fobj.write(line)

    def process_exception(self, request, exception, spider):
        log.info('exception {}'.format(exception))
        if isinstance(exception, self.IP_ERRORS):
            self.update_setting()
            self.process_request(request, spider)
