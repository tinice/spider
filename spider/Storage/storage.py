# -*- coding:utf-8 -*-
from DB import Db
db = Db()


def insertdb(sql):
    '''
    将数据插入数据库
    :param sql: 插入数据的sql语句
    :return:
    '''
    db.insert(sql)


def inserttxt(path, info):
    '''
    将数据写入txt文件
    :param path: txt文件路径
    :param info: 要写入文件的数据
    :return:
    '''
    with open(path, 'a+') as f:
        f.write(info + '\n')
