# -*- coding:utf-8 -*-
import time
from redis import Redis
from configure import ip
from multiprocessing import Pool

r = Redis(ip)


def Process(tar, name, tar2=None, tar3=None, tar4=None):
    p = Pool(processes=20)
    for i in range(100000):
        kw = r.spop(name)
        if kw == None:
            print '{} is None'.format(name)
            break
        p.apply_async(tar, args=(kw,))
        if tar2:
            p.apply_async(tar2, args=(kw,))
        time.sleep(0.1)
    p.close()
    p.join()
