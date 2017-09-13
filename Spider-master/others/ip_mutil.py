from bs4 import BeautifulSoup
import requests
import logging 
import os
import json
import time
import re
import threading

PROXY_SOURCE=[]
NUM=0

#快代理可一次获取多页,注意需睡眠1s
def get_freeproxy_in_kuaidaili(n):
    global PROXY_SOURCE
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
        PROXY_SOURCE.append(data)
 
 #讯代理一次只能获取一页，每10s更新,页面返回为json
def get_freeproxy_in_xdaili():
    global PROXY_SOURCE
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
        print(ip_proxy + " 该代理ip无效或响应过慢！")
def check_proxy_2(ip_proxy): 
    headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.baidu.com",
    "DNT":1,
    "Pragma": "no-cache",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Referer": "https://www.baidu.com/"
    }       
    proxy_host={"http":ip_proxy}
    try:
        resp0=requests.get(url="http://www.baidu.com/", proxies=proxy_host, timeout=20)
        resp1=requests.get(url="http://www.qq.com/", proxies=proxy_host, timeout=20)
        if resp0.status_code == requests.codes.ok and resp1.status_code == requests.codes.ok:
        	return True
            # print(proxy_host,"ok")
        else:
        	return False
            # print(proxy_host,"error")
    except Exception as e:
    	return False
        # print(e)


def proxy_main():
	global PROXY_SOURCE
	#get proxies
	#代理数小于3获取新的代理
	while True:
		if len(PROXY_SOURCE)<3:
			time.sleep(2)
			get_freeproxy_in_xdaili()
		porxy_info = PROXY_SOURCE.pop()
		proxy = porxy_info['ip'] + ":" + porxy_info['port']
		if check_proxy_2(proxy):
			return {"http":proxy}
		else:
			pass	

def main():
	for i in range(0,50):
		print(proxy_main())
		print(i)


if __name__ == '__main__':
    
    #日志模块初始化，日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
    logging.basicConfig(level=logging.DEBUG,
                format='%(message)s',
                datefmt= '%S',
                filename='debug2.log',
                filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.getLogger('requests').setLevel(logging.WARNING)

    '''threads_count=0;
    threads=[]

    start=time.clock()

    #only do once in 10s
    new_thread=threading.Thread(get_freeproxy_in_xdaili())
    threads.append(new_thread)
    threads_count=threads_count+1

    # for i in range(1,2):
    #     new_thread=threading.Thread(get_freeproxy_in_kuaidaili(i))
    #     threads.append(new_thread)
    #     threads_count=threads_count+1

    for i in range(0,threads_count):
        threads[i].start()

    for i in range(0,threads_count):
        threads[i].join()

    print("抓取完成")

    #检查ip是否有效

    second_threads=[]
    threads_count=0
    for index,item in enumerate(PROXY_SOURCE,0):
        ip_proxy=PROXY_SOURCE[index]['ip']+":"+PROXY_SOURCE[index]['port']
        new_thread=threading.Thread(check_proxy_2(ip_proxy))
        second_threads.append(new_thread)
        threads_count=threads_count+1
        
    for i in range(0,threads_count):
        second_threads[i].start()

    for i in range(0,threads_count):
        second_threads[i].join()

    end=time.clock()'''
    start=time.clock()
    main()
    end=time.clock()
    print('cost {0}s'.format(end - start))

  
