my_host = 'localhost'  # your host, usually localhost
my_user = 'root'     # your host, usually localhost
my_passwd = 'woaini1314' # your password
my_db = 'SPIDER' # name of the data base
DROP_OLD_TABLE = False #delete old table
table_name = 'movie_80s'

create_table_sql = """CREATE TABLE movie_80s
                      (
                        id        int             NOT NULL AUTO_INCREMENT,
                        name      nvarchar(100)   NOT NULL ,
                        types     nvarchar(50)    NULL,
                        language  nvarchar(50)    NULL,
                        actors    nvarchar(5000)  NULL,
                        director  nvarchar(50)    NULL,
                        show_time nvarchar(50)    NULL,
                        update_time  nvarchar(50) NULL,
                        duartion  nvarchar(50)    NULL,
                        short_des nvarchar(5000)  NULL,
                        long_des  nvarchar(10000) NULL,
                        img       nvarchar(100)   NULL,
                        PRIMARY KEY (id)
                      ) ENGINE=InnoDB;"""


def fillup_insert_command(data):
        value = {'name':None,'types':None,'language':None,'actors':None,'director':None,'show_time':None,'update_time':None,'duartion':None,'short_des':None,'long_des':None,'img':None}
        for key,val in data.items():
            if key == 'name':
                value['name'] = str(val).replace('\'',' ')
            if key == '类型：':
                value['types'] = val
            if key == '语言：':
                value['language'] = val
            if key == 'actors':
                value['actors'] = str(val).replace('\'',' ')
            if key == '导演：':
                value['director'] = str(val).replace('\'',' ')
            if key == '上映日期：':
                value['show_time'] = val
            if key == '更新日期：':
                value['update_time'] = str(val).replace('\'',' ')
            if key == '片长：':
                value['duartion'] = str(val).replace('\'',' ')
            if key == 'short_description':
                value['short_des'] = str(val).replace('\'',' ')
            if key == 'long_description':
                value['long_des'] = str(val).replace('\'',' ')
            if key == 'img':
                value['img'] = str(val).replace('\'',' ')
        command = "INSERT INTO movie_80s VALUES(NULL,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(value['name'],value['types'],value['language'],value['actors'],value['director'],value['show_time'],value['update_time'],value['duartion'],value['short_des'],value['long_des'],value['img'])
        return command
