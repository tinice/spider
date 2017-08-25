# -*- coding:utf-8 -*-
'''
对集合进行增删查改
'''
from Urlmanager import urlmanger
a = urlmanger.Uulmanger()


def del_info(name):
    print a.del_set(name)


def member(name):
    print a.urls_member(name)


def num(name):
    print a.url_size(name)


if __name__ == '__main__':
    name = 'encyclopedia_base_info'
    num(name)
