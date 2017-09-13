# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import json
from bs4 import BeautifulSoup
from config import HEADER
from proxy import Proxy
import os


class NeteaseMusic(object):
    """docstring for NeteaseMusic"""

    def __init__(self):
        # path = "C:\Program Files (x86)\Google\Chrome\chromedriver"
        # self.driver = webdriver.Chrome(executable_path=path)

        self.offset_list = []
        self.data = []
        self.proxy_list = []
        '''logging module'''

        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('debug.log')
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        fh.setFormatter(formatter)
        formatter = logging.Formatter("%(module)s:%(lineno)s %(funcName)s %(message)s")
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        logging.getLogger("requests").setLevel(logging.WARNING)

        self.proxy_spider = Proxy()
        self.update_proxy()
        self.import_proxy()
        self.update_driver()

    
    def get_detail_info(self, url):
        count = 0
        while True:
            try:
                count += 1
                self.driver.get(url)
                # self.logger.info(self.driver.title)
                self.driver.switch_to.frame("g_iframe")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#song-list-pre-cache > div > div > table > tbody > tr"))
                )
            except Exception as e:
                self.logger.info("serious error happened {0}".format(e))
                if len(self.proxy_list) < 1:
                    self.use_proxy()
                self.driver.quit()
                self.update_driver()
            else:
                break
            finally:
                if count >= 3:
                    return
        count = 0
        while 1:
            count += 1
            try:
                web = self.driver.page_source
            except Exception as e:
                self.logger.info("web page source error {0}".format(e))
            soup = BeautifulSoup(web, 'lxml')
            element = soup.select("#song-list-pre-cache > div > div > table > tbody > tr")
            if len(element):
                break
            if count > 10:
                return
          
        for one in element:
            try:
                tmp_a = one.select("span.txt > a")[0]
                tmp_span = one.select("td:nth-of-type(4) > div > span > a")[0]
                tmp_div = one.select("td:nth-of-type(5) > div > a")[0]
                temp_data = {
                    'song_id': tmp_a['href'],
                    'song_name': tmp_a.text,
                    'song_length': one.select("span.u-dur")[0].text,
                    'singer_name': tmp_span.text,
                    'singer_id': tmp_span['href'],
                    'album_name': tmp_div.text,
                    'album_id': tmp_div['href']
                }
                self.data.append(temp_data)
            except IndexError as e:
                pass
                # self.logger.info("{0} {1}".format(e, url))

    def import_offset(self,index):
        with open('./json/result{0}.json'.format(index), 'r') as fobj:
            self.offset_list = json.load(fobj)
        #self.offset_list = self.offset_list[0:20]
        self.logger.info(len(self.offset_list))
        self.logger.info('load json success')

    def use_proxy(self):
        self.driver.quit()
        self.update_proxy()
        self.import_proxy()

    def update_proxy(self):
        self.proxy_spider.get_proxy()
        self.logger.info('update proxy')
        
    def import_proxy(self):
        with open('./proxy.json','r') as fobj:
            self.proxy_list = json.load(fobj)

    def update_driver(self):
        proxy=self.proxy_list.pop()
        service_args = [
        '--proxy={0}:{1}'.format(proxy['ip'],proxy['port']),
        '--proxy-type={0}'.format(proxy['type']),
        ]
        for key, value in enumerate(HEADER):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.loadImages"] = False
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, service_args=service_args)
        self.driver.set_page_load_timeout(5)
        self.logger.info('update driver, left {0} avaliable'.format(len(self.proxy_list)))
    def grasp_main(self):
        base_url = "http://music.163.com"
		
        index = 11
        while index > 0:
            self.import_offset(index)
            self.logger.info('index = {0}'.format(index))
            count = 0
            for offset in self.offset_list:
                name = offset['href'][offset['href'].find('=') + 1:]
                self.get_detail_info(base_url + offset['href'])
                self.data.append(offset)
                with open('{0}.json'.format(name), 'w') as fobj:
                    json.dump(self.data, fobj)
                    self.data = []
                    self.logger.info('3 {0} process finish'.format(name))
                count += 1
                if len(self.proxy_list) < 1:
                    self.update_proxy()
                    self.import_proxy()
                if count > 20:
                    count = 0
                    self.driver.quit()
                    self.update_driver()
            os.system('rm proxy.json')
            os.system('mv *.json ./netease')
            os.system('tar -czvf result{0}.tgz ./netease'.format(index)) 
            os.system('rm ./netease/*')
            self.logger.info('index = {0} compress successed'.format(index))
            index -= 1
def test_json():
    with open('572217819.json', 'r') as fobj:
        offset = json.load(fobj)
    print(offset)


if __name__ == '__main__':
    start = time.time()
    mymusic = NeteaseMusic()
    mymusic.grasp_main()
    end = time.time()
    print(end - start)
