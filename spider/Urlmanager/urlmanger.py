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
        '''
        取出一个集合中的一个元素并删除
        :return:
        '''
        self.r.spop(name)

    def add_err_url(self, errname, url):
        '''
        :param errname: 存取请求失败url的集合名称
        :param url: 请求失败的url
        :return:
        '''
        self.r.sadd(errname, url)

    def url_size(self, name):
        '''
        查看某集合元素的个数
        :return:
        '''
        return self.r.scard(name)

    def urls_member(self, name):
        '''
        返回某集合所有的元素
        :return:
        '''
        return self.r.smembers(name)

    def del_set(self, name):
        '''
        删除某集合
        :return:
        '''
        self.r.delete(name)

    def del_keys(self):
        '''
        删除所有集合
        :return:
        '''
        keys = self.r.keys()
        self.r.delete(*keys)

