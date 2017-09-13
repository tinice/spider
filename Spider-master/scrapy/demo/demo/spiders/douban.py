import scrapy
from demo.identify_code import recognize_url


class MailSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['accounts.douban.com', 'douban.com']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'accounts.douban.com',
    }

    formdata = {
        'form_email': 'account',
        'form_password': 'password',
        'login': '登录',
        'redir': 'https://www.douban.com/',
        'source': 'None',
        'remember': 'on'
    }

    def start_requests(self):
        return [scrapy.Request(url='https://www.douban.com/accounts/login',
                               headers=self.headers,
                               meta={'cookiejar': 1, 'dont_redirect': True, 'handle_httpstatus_list': [302]},
                               dont_filter=True,
                               callback=self.parse_login)]

    def parse_login(self, response):
        self.log('parse_login url = {}'.format(response.url))
        if 'captcha_image' in response.text:
            print('Copy the link:')
            link = response.xpath('//img[@class="captcha_image"]/@src').extract()[0]
            print(link)
            recognize_url(link)
            captcha_id = link[link.find('id=') + 3:link.find('&')]
            print(captcha_id)
            captcha_solution = input('captcha-solution:')
            self.formdata['captcha-solution'] = captcha_solution
            self.formdata['captcha-id'] = captcha_id
        else:
            print('no captcha')
        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.formdata,
                                                 headers=self.headers,
                                                 meta={'cookiejar': response.meta['cookiejar'], 'dont_redirect': True,
                                                       'handle_httpstatus_list': [302]},
                                                 callback=self.after_login
                                                 )]

    def after_login(self, response):
        self.log('after login {}'.format(response.status))
        self.headers['Host'] = "www.douban.com"
        return scrapy.Request(url='https://www.douban.com/people/158339830/',
                              meta={'cookiejar': response.meta['cookiejar']},
                              headers=self.headers,
                              dont_filter=True,
                              callback=self.check_login)

    def check_login(self, response):
        self.log('check login {}'.format(response.url))
        if 'redir' in response.url:
            # login failed ,retry
            return [scrapy.Request(url='https://www.douban.com/accounts/login',
                                   headers=self.headers,
                                   meta={'cookiejar': 1},
                                   dont_filter=True,
                                   callback=self.parse_login)]
        else:
            self.log(response.headers)
            # login success, do something
            pass


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
