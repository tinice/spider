from bs4 import BeautifulSoup
import requests
import logging
import time
import asyncio

movie_info=[]
async def get_movie_info(orginal_url):
    loop = asyncio.get_event_loop()
    future= loop.run_in_executor(None,requests.get,orginal_url)
    web=await future
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    movie=soup.select("body > div > div > div > ul.me1.clearfix > li")
    for i in movie:
        try:
            tmp_dict={}
            tmp=i.select('a')
            tmp_url=tmp[0]['href']
            tmp_dict['offset']=tmp_url
            tmp_name=tmp[1].text.strip()
            tmp_dict['name']=tmp_name
            tmp_score=i.select('a > span.poster_score')[0].text
            tmp_dict['score']=tmp_score
            #tmp_dict['download_link']=get_movie_download_url(tmp_dict['offset'])
            movie_info.append(tmp_dict)
        except Exception as e:
            logging.warning("{0} {1}".format(e,tmp))


async def get_movie_download_url(i):
    orginal_url='http://www.80s.tw'+i['offset']
    loop = asyncio.get_event_loop()
    future= loop.run_in_executor(None,requests.get,orginal_url)
    web=await future
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'html.parser')
    try:
        download_link=soup.find("span",class_="xunlei dlbutton1").find('a')['href']
        i['link']=download_link
        logging.debug(i)
    except AttributeError as e:
        logging.warning('AttributeError url={0}'.format(orginal_url))

def get_page_length(orginal_url):
    web=requests.get(orginal_url)
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    length=soup.select("body > div > div > div > div.pager > a")[-1]['href']
    length=length[length.find('p')+1:]
    return int(length)

if __name__ == '__main__':
    
    #日志模块初始化，日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
    logging.basicConfig(level=logging.DEBUG,
                format='%(message)s',
                datefmt= '%S',
                filename='debug.log',
                filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.getLogger('requests').setLevel(logging.WARNING)

    fist_url="http://www.80s.tw/movie/list"

    page_len=get_page_length(fist_url)
    logging.info('{0} pages detected'.format(page_len))
    #get first page info
    get_movie_info(fist_url)

    loop = asyncio.get_event_loop()
    tasks=[]
    start=time.clock()
    for i in range(2,10):
        next_url="http://www.80s.tw/movie/list/-----p"+str(i)
        logging.info(next_url)
        tasks.append(get_movie_info(next_url))

    loop.run_until_complete(asyncio.wait(tasks))

    tasks2=[]
    #loop2 = asyncio.get_event_loop()
    count=0
    for i in movie_info:
        count=count+1
        tasks2.append(get_movie_download_url(i))

    loop.run_until_complete(asyncio.wait(tasks2))    
    end=time.clock()
    logging.info('cost {0}s'.format(end - start))
    loop.close()
  
