# -*- coding:utf-8 -*-
import dataoutput
import requests
from Process import process


def get_html(url):
    try:
        response = requests.get(url)
    except:
        return 'request fail'
    if '百度百科错误页' in response.content:
        return None
    html = response.content
    dataoutput.add_html('encyclopedia_html', html)


def main():
    process.Process(get_html, 'encyclopedia_url')


if __name__ == '__main__':
    main()
