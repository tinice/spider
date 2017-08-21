# -*- coding:utf-8 -*-
from storage import insertdb, inserttxt
from Process import process
from multiprocessing import Lock
from redis import Redis
from configure import ip
r = Redis(ip)
l = Lock()


def storage1(base_info):
    l.acquire()
    inserttxt('E:\ency\encyclopedia_base.txt', base_info)
    l.release()


def storage2(brief_info):
    l.acquire()
    inserttxt('E:\ency\encyclopedia_brief.txt', brief_info)
    l.release()


def main():
    process.Process(storage1, 'encyclopedia_base_info')
    process.Process(storage2, 'encyclopedia_brief_info')


if __name__ == '__main__':
    main()
    # storage1('encyclopedia_base_info')
