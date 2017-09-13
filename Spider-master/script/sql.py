import MySQLdb
import json
from sql_command import my_host,my_user,my_passwd,my_db,create_table_sql,table_name,fillup_insert_command,DROP_OLD_TABLE


class MySQLDB(object):
    """docstring for MySQLDB"""
    _instance = None
    def __new__(cls,*args,**kargv):
        if not cls._instance:
            cls._instance = super(MySQLDB, cls).__new__(cls, *args, **kargv)
        return cls._instance

    def __init__(self):
        self._db = MySQLdb.connect(host=my_host,   
                                user=my_user,         
                                passwd=my_passwd,  
                                db=my_db)        
        self._cur = self._db.cursor()

        # support chinese language
        self._db.set_character_set('utf8')  
        self._cur.execute('SET NAMES utf8;')  
        self._cur.execute('SET CHARACTER SET utf8;')  
        self._cur.execute('SET character_set_connection=utf8;')

        

    def create_table(self):
        # drop old table if exists
        if DROP_OLD_TABLE:
            drop_tables = "DROP TABLE IF EXISTS {}".format(table_name)
            self._cur.execute(drop_tables)
            self._db.commit()
            
        try:
            self._cur.execute(create_table_sql)
        except Exception as e:
            print(create_table_sql)
            print(e)
            raise e

    def query_info_re(self,colnums = '*',key='id' ,reg_exp='*'):
        try:
            command = "SELECT {} FROM {} WHERE {} REGEXP '{}'".format(colnums,table_name,key,reg_exp)
            self._cur.execute(command)
        except Exception as e:
            print(command)
            print(e)
            raise e
        return self._cur.fetchall()

    def insert_values(self,data):
        command = fillup_insert_command(data)
        try:
            self._cur.execute(command)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            print(command)
            print(e)
            raise e

    def __del__(self):
        self._db.close()
    
if __name__ == '__main__':
    import re
    import collections
    sql = MySQLDB()
    # sql.create_table()
    # with open('info_0.json','r') as fobj:
    #     for one in fobj:
    #         data = json.loads(one)
    #         sql.insert_values(data)
    res = sql.query_info_re(colnums='show_time',key='id',reg_exp='999*')
    p = []
    for one in res:
        p.append(re.sub('\D','',one[0]))
    res = collections.Counter(p)
    print(res)
