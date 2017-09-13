#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json


Base = declarative_base()
class Movie(Base):
    # 表的名字:
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    types = Column(String(50))
    language = Column(String(50))
    actors = Column(String(2000))
    director = Column(String(200))
    show_time = Column(String(50))
    update_time = Column(String(50))
    duartion = Column(String(50))
    short_des = Column(String(5000))
    long_des = Column(String(8000))
    img = Column(String(100))

    def __repr__(self):
        return '{}({} {})'.format(self.__class__.__name__, self.name,self.id)


user='root'
passwd = 'woaini1314'
host = 'localhost'
db='SPIDER'
class MySQLDB(object):
    _instance = None
    def __new__(cls,*args,**kargv):
        if not cls._instance:
            cls._instance = super(MySQLDB, cls).__new__(cls, *args, **kargv)
        return cls._instance

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}?charset=utf8'.format(user,passwd,host,db),echo=True)     
        Session = sessionmaker(bind = self.__engine)
        self.__session = Session()
        Base.metadata.create_all(self.__engine)
        self.__session.execute("alter database {} character set utf8".format(db))
        self.__session.execute("SET names 'utf8'")
        self.__session.execute("SET CHARACTER SET utf8")
        

    def insert_data(self,data):
        if isinstance(data,Movie):
            self.__session.add(data)
            self.__session.commit()
        else:
            raise TypeError

    #{id:10}
    def query(self):
        p = self.__session.query(Movie).filter_by(id=100).all()
        for one in p:
            print(one)
    
    def __del__(self):
        self.__session.close()


def fillup_insert_command(data):
        value = Movie()
        for key,val in data.items():
            if key == 'name':
                value.name = str(val).replace('\'',' ')
            if key == '类型：':
                value.types = val
            if key == '语言：':
                value.language = val
            if key == 'actors':
                value.actors = str(val).replace('\'',' ')
            if key == '导演：':
                value.director = str(val).replace('\'',' ')
            if key == '上映日期：':
                value.show_time = val
            if key == '更新日期：':
                value.update_time = str(val).replace('\'',' ')
            if key == '片长：':
                value.duartion = str(val).replace('\'',' ')
            if key == 'short_description':
                value.short_des = str(val).replace('\'',' ')
            if key == 'long_description':
                value.long_des = str(val).replace('\'',' ')
            if key == 'img':
                value.img = str(val).replace('\'',' ')
        return value

if __name__ == '__main__':
    sql = MySQLDB()
    with open('info_0.json','r') as fobj:
        for one in fobj:
            data = json.loads(one)
            sql.insert_data(fillup_insert_command(data))
    sql.query()
