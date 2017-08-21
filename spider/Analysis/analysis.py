# -*- coding:utf-8 -*-
from redis import Redis
from configure import ip
r = Redis(ip)


def add_kw(name, kw):
    r.sadd(name, kw)
