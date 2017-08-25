# -*- coding:utf-8 -*-
from urlmanger import Uulmanger
um = Uulmanger()
name = 'encyclopedia_url'


def main():
    '''
    获取百度百科词条的url
    :return:
    '''
    for i in range(50):
        url = 'http://baike.baidu.com/view/{0}.html'.format(i)
        um.add_new_url(name, url)


if __name__ == '__main__':
    main()
