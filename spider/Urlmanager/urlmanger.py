# -*- coding:utf-8 -*-
from redis import Redis
from configure import ip


class Uulmanger:
    def __init__(self):
        self.r = Redis(ip)

    def add_new_url(self, name, url):
        '''
        :param name: 'name'为爬取网页名称 + '_url', 'url'为获取的url
        :param url:
        :return:
        '''
        self.r.sadd(name, url)

    def get_url(self, name):
        self.r.spop(name)

    def add_err_url(self, errname, url):
        self.r.sadd(errname, url)

    def url_size(self, name):
        return self.r.scard(name)

    def urls_member(self, name):
        return self.r.smembers(name)

    def del_set(self, name):
        self.r.delete(name)

