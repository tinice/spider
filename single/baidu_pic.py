#!/usr/local/env python
# -*- coding:utf-8 -*-
import requests
import re


# 获取每页图片的访问链接
def get_page():
    urls = ['http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%e6%89%8b%e6%8b%bf%e7%93%b6%e5%ad%90&pn={}&gsm=3c00000000003c'.format(num) for num in range(0, 20000)]
    for url in urls:
        print(url)
        get_img_link(url)


# 从网页中获取每个图片的访问链接
def get_img_link(url):
    r = requests.get(url, verify=False)
    # print(r.encoding)
    r.encoding = 'utf-8'
    html_code = r.text
    reg = re.compile(r'"objURL":"(.*?)"')
    imgs = re.findall(reg, html_code)
    # print(imgs)
    for img in imgs:
        # print(img)
        down_img(img)


# 图片下载保存再本地
def down_img(url):
    web_data = requests.get(url, verify=False)
    filename = url.split('/')[-1]
    targetfile = 'E:/pict_baidu/{}'.format(filename)
    with open(targetfile, 'wb') as f:
        f.write(web_data.content)

if __name__ == '__main__':
    get_page()
