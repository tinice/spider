from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging as log
from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse
from flac.config import HEADER
import pymongo


class CustomNormalMiddleware(object):
    def __init__(self):
        # url = 'mongodb://xxx:xxx@ip:27017/db_name'
        # self.client = pymongo.MongoClient(url)

        # self.client = pymongo.MongoClient("localhost", 27017)
        # self.db = self.client.proxy
        # self.collection = self.db.proxy

        self.proxy = None
        self._count = 0
        # every 20 times change a proxy
        self._threshold = 20
        # self.update_proxy()

    def process_request(self, request, spider):
        if 'hiflac' in request.url:
            self._count += 1
            if self._count > self._threshold:
                self._count = 0
                # self.update_proxy()
            # request.meta['proxy'] = "http://{0}:{1}".format(self.proxy['ip'], self.proxy['port'])
            request.meta['proxy'] = "http://123.163.19.201:23128"

    def update_proxy(self):
        self.proxy = self.collection.findOne()
        self.collection.remove(self.proxy)
        log.info('update proxy')


class CustomsSleniumMiddleware(object):
    def __init__(self):
        # Do not load images
        # url = 'mongodb://xxx:xxx@ip:27017/db_name'
        # self.client = pymongo.MongoClient(url)

        # self.client = pymongo.MongoClient("localhost", 27017)
        # self.db = self.client.proxy
        # self.collection = self.db.proxy
        self.proxy = None
        self.driver = None
        # self.update_proxy()

        self._count = 0
        self._cap = webdriver.DesiredCapabilities.PHANTOMJS
        self._cap["phantomjs.page.settings.loadImages"] = False
        self.update_driver()

    def update_driver(self):
        self.update_proxy()
        service_args = [
            '--proxy={0}:{1}'.format(self.proxy['ip'], self.proxy['port']),
            '--proxy-type={0}'.format(self.proxy['type']),
        ]
        for key, value in enumerate(HEADER):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        self.driver = webdriver.PhantomJS(desired_capabilities=self._cap, service_args=service_args)
        self.driver.set_page_load_timeout(5)

    def use_proxy(self):
        if True:
            return True
        else:
            return False

    def update_proxy(self):
        self.proxy = self.collection.findOne()
        self.collection.remove(self.proxy)
        log.info('update proxy')

    def process_request(self, request, spider):
        if self.use_selenium(request.url):
            if self.use_proxy():
                if self._count > 20:
                    self.update_driver()
                    self._count = 0
                    log.info('update driver')
            yield HtmlResponse(request.url, encoding='utf-8', body=self.driver.page_source.encode('utf8'))

    def use_selenium(self, url):
        count = 0
        while True:
            try:
                count += 1
                self.driver.get(url)
                self.driver.switch_to.frame("g_iframe")
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#song-list-pre-cache > div > div > table > tbody > tr"))
                )
            except Exception as e:
                log.info("selenium serious error happened {0}".format(e))
            else:
                if self.source_code_ok():
                    return True
                else:
                    return False
            finally:
                if count >= 3:
                    log.info('selenium try three time,not again')
                    return None

    def source_code_ok(self):
        count = 0
        while 1:
            count += 1
            try:
                web = self.driver.page_source
            except Exception as e:
                log.info("web page source error {0}".format(e))
            soup = BeautifulSoup(web, 'lxml')
            element = soup.select("#song-list-pre-cache > div > div > table > tbody > tr")
            if len(element):
                return True
            if count > 10:
                return False
