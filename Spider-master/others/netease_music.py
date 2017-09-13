from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import music
import multiprocessing
import logging
import json

class NeteaseMusic(object):
    """docstring for NeteaseMusic"""
    def __init__(self):
        #path="C:\Program Files (x86)\Google\Chrome\chromedriver"
        #self.driver = webdriver.Chrome(executable_path=path)
         
        self.playlist=[]
        self.idlist=[]

        '''logging module'''

        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG) 

        fh = logging.FileHandler('detail_info.log') 
        ch = logging.StreamHandler() 
        ch.setLevel(logging.INFO) 
        formatter = logging.Formatter('%(message)s') 
        fh.setFormatter(formatter) 
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh) 
        self.logger.addHandler(ch)
        #logging.getLogger("requests").setLevel(logging.WARNING)

        # self.pool=multiprocessing.Pool(processes=2)
        

    def proc_playlist(self,tmp_playlist):
        for tmp in tmp_playlist:
            if tmp['href'] not in self.idlist:
                self.playlist.append(tmp)
                self.idlist.append(tmp['href'])
                #self.logger.debug(tmp)
                self.logger.debug(tmp['href'])
            else:
                pass
    def grasp_overall_playlist(self):
        urls=music.get_urls()
        total_length=0

        for url in urls:
            pool= multiprocessing.Pool(processes=32)
            length=music.get_length(url+'0')
            total_length+=length
            for offset in range(0,length):
                pool.apply_async(music.get_palylist_overall_info,args=(url+str(offset*35),),callback=self.proc_playlist)
            self.logger.info(url)
            pool.close()
            pool.join()
            time.sleep(20)

        count = 0 
        while count* 1000< len(self.playlist):
            start = count * 10000
            end = (count+1) * 10000

            if end > len(self.playlist):
                end=len(self.playlist)

            with open('result{0}.json'.format(count),'w') as fobj:
                json.dump(self.playlist[start:end],fobj)
            count = count+1
        self.logger.info(len(self.playlist))
        self.logger.info("total playlist page len={0}".format(total_length))


def get_detail_info(driver,offset):
    '''get netease music playlist info'''
    print("87")
    base_url="http://music.163.com"
    url=base_url+offset
    result = []
    driver.get(url)
    print(driver.title)
    driver.switch_to_frame("g_iframe")

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#song-list-pre-cache > div > div > table > tbody > tr"))
    )
    
    element = driver.find_elements_by_css_selector("#song-list-pre-cache > div > div > table > tbody > tr")
    for one in element:
        try:
            data={
            'song_id':one.find_elements_by_css_selector("span.txt > a")[0].get_attribute('href'),
            'song_name':one.find_elements_by_css_selector("span.txt > a")[0].text,
            'song_length':one.find_elements_by_css_selector("span.u-dur")[0].text,
            'singer_name':one.find_elements_by_css_selector("td:nth-child(4) > div > span > a")[0].text,
            'singer_id':one.find_elements_by_css_selector("td:nth-child(4) > div > span > a")[0].get_attribute('href'),
            'album_name':one.find_elements_by_css_selector("td:nth-child(5) > div > a")[0].text,
            'album_id':one.find_elements_by_css_selector("td:nth-child(5) > div > a")[0].get_attribute('href')
            }
            result.append(data)
        except Exception as e:
            print("{0} occur error {1}".format(data,e))
    with open('{0}.json'.format(offset[offset.find('=')+1:]),'w') as fobj:
            json.dump(result,fobj)
    print("{0} is fininsh\n".format(offset))

def grasp_main():
    count = 11
    
    driver=webdriver.PhantomJS()
    while count:
        with open("result{0}.json".format(count),'r')  as fobj:
            data_list = json.load(fobj)
        print(len(data_list))
        count = count -1
        pool= multiprocessing.Pool()
        for data in data_list:
            pool.apply_async(get_detail_info, args=(driver,data['href'],))
        pool.close()
        pool.join()
        break
        time.sleep(20)
    driver.quit()
if __name__ == '__main__':
    start = time.time()
    #mymusic=NeteaseMusic()
    grasp_main()

    end = time.time()
    print(end-start)
