# -*- coding:utf-8 -*-
import requests
from lxml import etree


cookies = {
    'cookie': '_T_WM=4e2ebab8ade3864f3a99988d6b9998e0; ALF=1502512797; SCF=Avij6Khf1BkvuDp5rOxhQPTN4JmraGIJfy68uT6PT2gmDYT0lRYfvW5zblzNU-M9JJr-Raq0g9lyTzcYx_RxE1M.; SUB=_2A250YonNDeRhGeVI6FUR8yfKyDmIHXVXrBeFrDV6PUJbktBeLWz4kW1fuTbihOp5E9T7frBvbhZZagMKOw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeP1M_d5p8IWBO1a4HxSkm5JpX5o2p5NHD95Q0SoeNehe4SoefWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNe0q0S0501Kq0SBtt; SUHB=0U1J--v9UOdzw4; SSOLoginState=1499920797'}


def get_url(big_id):
    headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Referer': 'https://weibo.cn/1261700994/fans'}
    url_list = []
    for i in range(1, 21):
        url = 'https://weibo.cn/{0}/fans?page={1}'.format(big_id, i)
        try:
            response = requests.get(url, headers=headers, cookies=cookies, verify=False, timeout=5)
        except:
            print i
            continue
        new_html = response.text.encode('utf-8').replace('<!--?xml version="1.0" encoding="UTF-8"?--><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">','')
        con = etree.HTML(new_html)
        id_list = con.xpath('//tr/td[1]/a[1]/@href')
        url_list.extend(id_list)
        # print id_list
    return url_list


def get_info(url):
    headers = {'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Referer': url}
    for h in range(1,21):
        new_url = url + '?page=' + str(h)
        try:
            response = requests.get(new_url, headers=headers, cookies=cookies, verify=False, timeout=5)
            html = response.text.encode('utf-8').replace(
            '<!--?xml version="1.0" encoding="UTF-8"?--><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
            '')
            r = etree.HTML(html)
            info = r.xpath('//span[@class="ctt"]/text()')
        except:
            break
        if info == []:
            break
        for i in info:
            if i == ' ':
                continue
            with open('weibo.txt', 'a+') as f:
                f.write(i.encode('utf-8').strip().replace('\n', ',') + '\n')


if __name__ == '__main__':
    aaa = '1563008055'
    url_list = get_url(aaa)
    for i in url_list:
        get_info(i)
# r = con.xpath('//span[@class="ctt"]/text()')
# print r
# for i in r:
#     if i == ' ':
#         continue
#     with open('aaa.txt', 'a') as f:
#         f.write(i.encode('utf-8').strip().replace('\n', ',') + '\n')
#     print i
