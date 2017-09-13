from bs4 import BeautifulSoup
import requests 
import os
import json
import time
import re
import gevent
from multiprocessing import Process

PROXY_SOURCE=[]
NUM=0

#快代理可一次获取多页,注意需睡眠1s
def get_freeproxy_in_kuaidaili(n):
    global NUM,PROXY_SOURCE
    orginal_url="http://www.kuaidaili.com/free/inha/"+str(n)+"/"
    web=requests.get(orginal_url)
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    things=soup.select('#list > table > tbody > tr')
    for one in things:
        tmp=one.select('td')
        data={
        'ip':tmp[0].text,
        'port':tmp[1].text,
        'anony':tmp[2].text,
        'type':tmp[3].text,
        'position':tmp[4].text,
        'response_time':tmp[5].text,
        'check_time':tmp[6].text
        }
        if data not in PROXY_SOURCE:
            PROXY_SOURCE.append(data)
 
 #讯代理一次只能获取一页，每10s更新,页面返回为json
def get_freeproxy_in_xdaili():
    global NUM,PROXY_SOURCE
    orginal_url="http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10"
    web=requests.get(orginal_url)
    web.encoding='utf-8'
    info=json.loads(web.text)
    info=info['rows']
    for one in info:
        data={
        'ip':one['ip'],
        'port':one['port'],
        'anony':one['anony'],
        'type':one['type'],
        'check_time':one['validatetime'],
        'position':one['position'],
        'response_time':one['responsetime']
        }
        if data not in PROXY_SOURCE:
            PROXY_SOURCE.append(data)
    
def check_proxy_1(ip):
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.1356789.com",
    "Pragma": "no-cache",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Referer": "http://m.ip138.com/"
    }
    try:
        proxy_host={"http":ip}
        resp = requests.get(url="http://www.1356789.com/", proxies=proxy_host, headers=headers, timeout=10)
        if resp.status_code == 200:
            page = resp.text
            ip_url = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', page).group()
            ip_now = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ip).group()
            if ip_url == ip_now:  # 判断是否是匿名代理
                print(ip + " 匿名代理")
            else:
                print(ip + " 透明代理")
    except Exception:
        #pass
        print(ip + " 该代理ip无效或响应过慢！")
def check_proxy_2(ip_proxy):
    proxy_host={"http":ip_proxy}
    try:
        #resp0=requests.get(url="http://www.baidu.com/", proxies=proxy_host, timeout=20)
        resp1=requests.get(url="http://www.qq.com/", proxies=proxy_host, timeout=20)
        #if resp0.status_code == requests.codes.ok and resp1.status_code == requests.codes.ok:
        if resp1.status_code == requests.codes.ok:
            print(proxy_host,"ok")
        else:
            print(proxy_host,"error")
    except Exception as e:
        print(e)

def validate(start,end):
    global NUM,PROXY_SOURCE
    threads=[]
    for index in range(start,end):
        ip_proxy=PROXY_SOURCE[index]['ip']+":"+PROXY_SOURCE[index]['port']
        try:
            threads.append(gevent.spawn(check_proxy_1,ip_proxy))
        except Exception as e:
            print(e)
    gevent.joinall(threads)

if __name__ == '__main__':
    start=time.time()
    tic = lambda: 'finish at %1.1f seconds' % (time.time() - start)
    for i in range(0,10):
        get_freeproxy_in_xdaili()
        time.sleep(15)
        get_freeproxy_in_kuaidaili(i)
    print("抓取完成")
    print("ip数量为{0}".format(len(PROXY_SOURCE)))
    print(tic())
    start=time.time()
    i=0
    while i < len(PROXY_SOURCE):
        p = Process(target=validate,args=(i,i+20))
        p.start()
        i=i+20
    print(tic())
  
