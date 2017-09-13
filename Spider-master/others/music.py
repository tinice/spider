from bs4 import BeautifulSoup
import multiprocessing
import requests
import json

def get_palylist_overall_info(orginal_url):
    playlists_overall_info=[]
    try:
        web=requests.get(orginal_url, timeout=400)
    except Exception as e:
        print("get_palylist_overall_info failed, {0} {1} url passed".format(orginal_url,e))
        return
    if web.status_code!=200:
        print("get_palylist_overall_info, stauts code don\'t match {0} ".format(orginal_url))
        return
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    playlists_row_data=soup.select('ul > li')
    for one in playlists_row_data:
        try:
            tmp={
            "img":one.select('div.u-cover.u-cover-1 > img')[0]['src'],
            "title":one.select('div.u-cover.u-cover-1 > a')[0]['title'],
            "href":one.select('div.u-cover.u-cover-1 > a')[0]['href'],
            "play_num":one.select('div.u-cover.u-cover-1 > div.bottom > span.nb')[0].text,
            }
        except IndexError as e:
            continue
        try:
           tmp["author"]=one.select('p:nth-of-type(2) > a')[0].text
        except Exception as e:
            print(e)
            pass
        playlists_overall_info.append(tmp)
    return playlists_overall_info
def get_length(orginal_url):
    try:
        web=requests.get(orginal_url, timeout=400)
    except Exception as e:
        print("get_palylist_overall_info failed, {0} {1} url passed".format(orginal_url,e))
        return
    if web.status_code!=200:
        print("get_palylist_overall_info, stauts code don\'t match {0} ".format(orginal_url))
        return
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    length=soup.select('#m-pl-pager > div > a')[-2].text
    title=soup.select("#m-disc-pl-c > div > div.u-title.f-cb > h3 > span")[0].text
    print(title)
    return int(length)
def get_url_list_overall(orginal_url="http://music.163.com/discover/playlist"):
    url_list=[]
    try:
        web=requests.get(orginal_url, timeout=400)
    except Exception as e:
        print("get_palylist_overall_info failed, {0} {1} url passed".format(orginal_url,e))
        return
    if web.status_code!=200:
        print("get_palylist_overall_info, stauts code don\'t match {0} ".format(orginal_url))
        return
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    raw_data=soup.select("#cateListBox > div.bd > dl")
    for one in raw_data:
        links=one.select('dd > a')
        for link in links:
            # data={
            # link.text:link['href']
            # }
            url_list.append(link['href'])
    return url_list

def get_urls():
        urls=get_url_list_overall()
        url_list=[]
        order_new_head="http://music.163.com/discover/playlist/?order=hot&"
        order_hot_head="http://music.163.com/discover/playlist/?order=new&"
        base_tail="&limit=35&offset="
        for one in urls:
            one=one[one.find('?')+1:]
            hot_url=order_hot_head+one+base_tail
            new_url=order_new_head+one+base_tail
            url_list.append(hot_url)
            url_list.append(new_url)
        return(url_list)

if __name__ == '__main__': 
    #get_palylist_overall_info()
    #get_length()
    get_urls()
    