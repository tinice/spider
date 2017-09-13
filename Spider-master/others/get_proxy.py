from bs4 import BeautifulSoup
import requests
import os
import json
import time
import re
import multiprocessing
import sched
from pymongo import *


class Proxy(object):
    """docstring for Proxy"""

    def __init__(self, num, pool_size):
        self.pool_size = pool_size
        res = self.db().find()
        for one in res:
            self.db().remove(one)
        if num == 0:
            self.run_num = 100000
        else:
            self.run_num = num * 2
        self.passed = []
        self.hot = []
        self.cold = []
        self.pending = []
        self.count = 0

        self.s2 = sched.scheduler(time.time, time.sleep)
        self.s2.enter(0, 1, self.get_freeproxy_in_xdaili)
        self.s2.enter(3, 1, self.grasp_proxy)
        self.s2.run()
        self.s1 = sched.scheduler(time.time, time.sleep)
        self.s1.enter(3600, 2, self.regular.clean)
        self.s1.run()

    def regular_clean(self):
        for one in res:
            self.db().remove(one)
        self.get_freeproxy_in_xdaili()
        self.grasp_proxy()
        self.cold = []
        if self.run_num:
            self.run_num -= 1
            self.s1.enter(3600, 2, self.regular.clean)

    def db(self):
        client = MongoClient('mongodb://poluo:poluo123@115.28.36.253:27017/proxy')
        db = client.proxy
        collection = db.proxy_list
        return collection

    def get_db_content(self):
        res = self.db().find()
        for one in res:
            print(one)

    def filter(self):
        pool = multiprocessing.Pool(processes=self.pool_size)

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        for index in range(len(self.pending)):
            if self.pending[index] not in self.cold and self.pending[index] not in self.passed:
                ip_proxy = self.pending[index]['ip'] + ":" + self.pending[index]['port']
                try:
                    pool.apply_async(self.validate_proxy, (ip_proxy, index, return_dict,))
                except:
                    pass
        pool.close()
        pool.join()
        results = return_dict.values()
        for i in range(len(results)):
            if results[i] == 1 and self.pending[i] not in self.passed:
                self.passed.append(self.pending[i])
                self.db().insert(self.pending[i])
        print("\npassed len={0}".format(len(self.passed)))
        for i in range(len(self.pending)):
            if self.pending[i] not in self.cold and self.pending[i] not in self.passed:
                self.cold.append(self.pending[i])
        print("cold len={0}".format(len(self.cold)))
        self.pending = []

    def grasp_proxy(self):
        self.count += 1
        if self.count % 2 == 0:
            tmp = 2
        else:
            tmp = 1
        self.get_freeproxy_in_xicidaili(tmp)
        # self.get_freeproxy_in_cnproxy()
        self.filter()
        if self.run_num:
            self.s2.enter(60, 1, self.grasp_proxy)
            self.run_num -= 1

    def validate_proxy(self, ip, index, return_dict):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.1356789.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Referer": "http://m.ip138.com/"
        }
        try:
            proxy_host = {"http": ip}
            resp = requests.get(url="http://www.1356789.com/", proxies=proxy_host, headers=headers, timeout=10)
            if resp.status_code == 200:
                page = resp.text
                ip_url = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', page).group()
                ip_now = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip).group()
                if ip_url == ip_now:
                    return_dict[index] = 1
                else:
                    return_dict[index] = 2
        except Exception:
            return_dict[index] = 3

    def get_freeproxy_in_xicidaili(self, i):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "www.xicidaili.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        }
        if i == 1:
            orginal_url = "http://www.xicidaili.com/nn/"
        else:
            orginal_url = "http://www.xicidaili.com/nn/" + str(i) + "/"
        web = requests.get(orginal_url, headers=headers)
        print(orginal_url)
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, 'lxml')
        things = soup.select('tr.odd')
        data = {}
        count = 0
        for one in things:
            try:
                tmp = one.select('td')
                data = {
                    'ip': tmp[1].text,
                    'port': tmp[2].text,
                    'anony': tmp[4].text,
                    'type': tmp[5].text,
                    'position': 'unknow',
                    'response_time': 'unknow',
                    'check_time': tmp[-1].text
                }
            except Exception as e:
                # print("{0}".format(e))
                pass
            count = count + 1
            if data != {} and data not in self.pending:
                self.pending.append(data)

    def get_freeproxy_in_cnproxy(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "cn-proxy.com",
            "Pragma": "no-cache",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
        }
        web = requests.get('http://cn-proxy.com/', headers=headers)
        print('http://cn-proxy.com/')
        soup = BeautifulSoup(web.text,'lxml')
        things = soup.select('tr')
        for one in things:
            tmp = one.select('td')
            try:
                data = {
                    'ip': tmp[1].text,
                    'port': tmp[2].text,
                    'anony': 'unknow',
                    'type': 'unknow',
                    'position': tmp[3].text,
                    'response_time': 'unknow',
                    'check_time': tmp[-1].text
                }
                print(data)
            except IndexError:
                pass



    def get_freeproxy_in_xdaili(self):
        orginal_url = "http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10"
        print(orginal_url)
        web = requests.get(orginal_url)
        web.encoding = 'utf-8'
        info = json.loads(web.text)
        info = info['rows']
        for one in info:
            data = {
                'ip': one['ip'],
                'port': one['port'],
                'anony': one['anony'],
                'type': one['type'],
                'check_time': one['validatetime'],
                'position': one['position'],
                'response_time': one['responsetime']
            }
            if data not in self.pending:
                self.pending.append(data)
        if self.run_num:
            self.s2.enter(600, 1, self.get_freeproxy_in_xdaili)
            self.run_num -= 1


if __name__ == '__main__':
    test = Proxy(0, 50)
