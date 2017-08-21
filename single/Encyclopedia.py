# -*- coding:utf-8 -*-
import time
import requests
from lxml import etree
# import MySQLdb
from DB import Db
import sys
sys.getdefaultencoding()

# con = MySQLdb.connect(host='localhost', user='root', passwd='', db='encyclopedia', port=3306, charset='utf8')
# cur = con.cursor()


class Encyclopedia:
    def __init__(self):
        self.db = Db()

    def get_result(self, kw_url):
        try:
            response = requests.get(kw_url)
        except:
            return 'request fail'
        if '百度百科错误页' in response.content:
            return None
        result = etree.HTML(response.content)
        return result

    def get_dict(self, result):
        if result is None:
            return None
        if result == 'request fail':
            return 'request fail'
        title = result.xpath('//dd[@class = "lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
        name = result.xpath('//div[@class = "basic-info cmn-clearfix"]//dt')
        if name == []:
            return None
        value = result.xpath('//div[@class = "basic-info cmn-clearfix"]//dd')
        name_list = []
        for i in name:
            name_list.append('' + i.xpath('string(.)'))
        value_list = []
        for k in value:
            value_list.append('' + k.xpath('string(.)').strip())
        info = ''
        for h in range(len(name_list)):
            info = info + name_list[h].encode('utf-8') + ':' + value_list[h].encode('utf-8') + ',    '
        base_info = title.encode('utf-8') + '  --  ' + info
        return base_info

    def brief_introduction(self, result):
        if result is None:
            return None
        try:
            title = result.xpath('//dd[@class = "lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
        except:
            return None
        company = result.xpath('//div[@class = "lemma-summary"]')
        brief_info = ''
        for k in company:
            brief_info = brief_info + k.xpath('string(.)').strip().replace('\n', '')
        brief_info = (title + ':' + brief_info).encode('utf-8')
        return brief_info

    def other_info(self, ):
        pass

    def insert_db(self, kw_url):
        i = kw_url[28:-5]
        result = self.get_result(kw_url)
        base_info = self.get_dict(result)
        if base_info is None:
            return
        if base_info == 'request fail':
            time.sleep(5)
            base_info = self.get_dict(result)
            if base_info == 'request fail':
                return
        brief_info = self.brief_introduction(result)
        try:
            sql = "insert into encyclopedia2 (id,base_info,brief_info) values ('%s','%s', '%s')" % (i, base_info, brief_info)
            self.db.insert(sql)
            # cur.execute(sql)
            # con.commit()
            time.sleep(0.3)
        except:
            print i
            return


if __name__ == '__main__':
    a = Encyclopedia()
    for i in range(0, 10):
        url = 'http://baike.baidu.com/view/{0}.html'.format(i)
        a.insert_db(url)

    # url = 'http://baike.baidu.com/view/{0}.html'.format(399)
    # result = get_result(url)
    # base_info = get_dict(result)
    # brief_info = brief_introduction(result)
    # # print base_info
    # # print brief_info
    # sql = "insert into encyclopedia (id,base_info,brief_info) values ('%s','%s', '%s')" % (399, base_info, brief_info)
    # cur.execute(sql)
    # con.commit()
