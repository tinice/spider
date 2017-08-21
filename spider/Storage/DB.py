# -*- coding:utf-8 -*-
import MySQLdb


class Db:
    def __init__(self):
        self.con = MySQLdb.connect(host='localhost', user='root', passwd='', db='encyclopedia', port=3306, charset='utf8')
        self.cur = self.con.cursor()

    def insert(self, sql):
        self.cur.execute(sql)
        self.con.commit()

if __name__ == '__main__':
    a = Db()
    base_info = '你好'
    a.insert("insert into encyclopedia (base_info) values ('%s')" % base_info)
