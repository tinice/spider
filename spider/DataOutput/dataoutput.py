# -*- coding:utf-8 -*-
from redis import Redis
from configure import ip
r = Redis(ip)


def add_html(name, html):
    '''
    :param name: name格式为'爬取内容名_html',eg:encyclopedia_html
    :return:
    '''
    r.sadd(name, html)
