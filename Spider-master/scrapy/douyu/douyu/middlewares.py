import logging as log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse


class CustomNormalMiddleware(object):
    def __init__(self):
        self.cookies = {'Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7': '1493130868,1493207155,1493209130',
                        'Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7': '1493209130',
                        '_dys_lastPageCode': 'page_classify,page_live',
                        '_dys_refer_action_code': 'init_page_live'}
        path = "C:\Program Files (x86)\Google\Chrome\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=path)

    def process_request(self, request, spider):
        try:
            selenium_enable = request.meta.get('selenium')
        except Exception as e:
            log.info(e)
            selenium_enable = False
        if selenium_enable:
            self.driver.get(request.url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "#js-fans-rank > div > div.f-con > div.f-cn.cur > ul > li> a"))
            )
            body = self.driver.page_source
            response = HtmlResponse(url=self.driver.current_url, body=body, request=request, encoding='utf8')
            return response
        else:
            request.headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            request.headers[
                'Accept'] = '*/*'
            request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
            request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
            request.headers['Connection'] = 'keep-alive'
            request.headers['Host'] = 'www.douyu.com'
            request.headers['Upgrade-Insecure-Requests'] = 1

            try:
                cookies_enable = request.meta.get('cookies')
            except Exception as e:
                log.info(e)
                cookies_enable = False
            if cookies_enable:
                del request.headers['Upgrade-Insecure-Requests']
                request.headers['DNT'] = '1'
                request.headers['X-Requested-With'] = 'XMLHttpRequest'
                request.headers['referer'] = request.meta['referer']
                self.cookies['_dys_lastPageCode'] = request.meta.get('_dys_lastPageCode')
                self.cookies['_dys_refer_action_code'] = request.meta.get('_dys_refer_action_code')
                request.cookies = self.cookies
