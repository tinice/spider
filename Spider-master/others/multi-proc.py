from bs4 import BeautifulSoup
import requests
import logging
import time
import multiprocessing

COUNT=0
def get_movie_info(n):
    global COUNT
    if n==1:
        orginal_url="http://www.80s.tw/movie/list"
    else:
        orginal_url="http://www.80s.tw/movie/list/-----p"+str(n)
    web=requests.get(orginal_url)
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'lxml')
    movie=soup.select("body > div > div > div > ul.me1.clearfix > li")
    for i in movie:
        try:
            tmp_dict={
            'offset':i.select('a')[0]['href'],
            'name':i.select('a')[1].text.strip(),
            'score':i.select('a > span.poster_score')[0].text
            }
            COUNT=COUNT+1
        except Exception as e:
            logging.warning("{0} {1}".format(e,tmp))

  
def get_movie_download_url(url):
    orginal_url='http://www.80s.tw'+url
    web=requests.get(orginal_url)
    web.encoding='utf-8'
    soup=BeautifulSoup(web.text,'html.parser')
    try:
        download_link=soup.find("span",class_="xunlei dlbutton1").find('a')['href']
        return download_link
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


    page_len=get_page_length("http://www.80s.tw/movie/list")
    logging.info('{0} pages detected'.format(page_len))
    #get first page info
    pool_size=10
    pool = multiprocessing.Pool(processes=pool_size)

    start=time.clock()
    for i in range(0,30):
        logging.info(i+1)
        pool.apply_async(get_movie_info,(i+1,))
    pool.close()
    pool.join()
  
    end=time.clock()
    print(COUNT)
    logging.info('cost {0}s'.format(end - start))
  
