# -*- coding:utf-8 -*-
from DB import Db
db = Db()


def insertdb(sql):
    db.insert(sql)


def inserttxt(path, info):
    with open(path, 'a+') as f:
        f.write(info + '\n')
