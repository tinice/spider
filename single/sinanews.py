# -*- coding:utf-8 -*-
import time
import re
import requests
from lxml import etree
from multiprocessing import Pool
import sys
sys.getdefaultencoding()


def get_url():
    url = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?col=89&spec=&type=&date=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=1'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'roll.news.sina.com.cn',
        'Referer': 'http://roll.news.sina.com.cn/s/channel.php?ch=01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    responses = requests.get(url, headers=headers)
    html = responses.text
    url_list = re.findall(r',url : "http(.*?)",type : ', html)
    return url_list


def get_info(url):
    responses = requests.get(url)
    html = etree.HTML(responses.content)
    info = html.xpath('//div[@id="artibody"]')[0]
    news = info.xpath('string(.)').strip().encode('utf-8')
    # print news
    name = int(time.time() * 1000)
    with open('F:\sinanews\{}.txt'.format(name), 'w+') as f:
        f.write(news + '\n\n' + url)

if __name__ == '__main__':
    url_list = get_url()
    p = Pool(processes=80)
    for i in url_list:
        url = 'http' + i.encode('utf-8')
        p.apply_async(get_info, args=(url,))
    p.close()
    p.join()
    # url = 'http://news.sina.com.cn/o/2017-07-26/doc-ifyihrwk2552980.shtml'
    # #url = 'http://finance.sina.com.cn/stock/usstock/c/2017-07-26/doc-ifyihrit1503860.shtml'
    # get_info(url)

