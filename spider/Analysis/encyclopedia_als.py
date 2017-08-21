# -*- coding:utf-8 -*-
from analysis import add_kw
from Process import process
from redis import Redis
from configure import ip
from lxml import etree
r = Redis(ip)


def get_dict(html):
    # html = r.spop('encyclopedia_html')
    result = etree.HTML(html)
    if result is None:
        return None
    if result == 'request fail':
        return 'request fail'
    try:
        title = result.xpath('//dd[@class = "lemmaWgt-lemmaTitle-title"]/h1/text()')[0]
    except:
        return None
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
    add_kw('encyclopedia_base_info', base_info)


def brief_introduction(html):
    result = etree.HTML(html)
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
    add_kw('encyclopedia_brief_info', brief_info)


def main():
    process.Process(get_dict, 'encyclopedia_html', brief_introduction)
    # process.Process(brief_introduction, 'encyclopedia_html')


if __name__ == '__main__':
    main()
