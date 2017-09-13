# -*- coding: utf-8 -*-
import scrapy
import re
import poplib
import time
import collections


class PeopleSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["linkedin.com"]
    public_id = re.compile('"publicIdentifier":"[^{}]*",')
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'Linkedin.middlewares.LoginMiddleware': 543,
                                   'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 500, },
        'DOWNLOAD_DELAY': 0,
        'COOKIES_DEBUG': False,
    }

    def start_requests(self):
        ACCOUNT = collections.namedtuple('ACCOUNT', ['user', 'passwd', 'email', 'email_passwd'])
        user = self.settings.getlist('USER')
        passwd = self.settings.getlist('PASSWD')
        email = self.settings.getlist('EMAIL')
        email_passwd = self.settings.getlist('EMAIL_PASSWD')
        _accounts = [ACCOUNT(user[i], passwd[i], email[i], email_passwd[i]) for i in range(len(user))]
        for one in _accounts:
            yield scrapy.Request(url='https://www.linkedin.com/uas/login', meta={'cookiejar': 1, 'data': one},
                                 callback=self.parse)

    def parse(self, response):
        data = response.meta.get('data')
        account = data[0]
        passwd = data[1]
        tmp = response.css('#login')
        is_js_enabled = tmp.css('input[type="hidden"]:nth-child(1)::attr(value)').extract_first()
        login_csrf_param = tmp.css('#loginCsrfParam-login::attr(value)').extract_first()
        source_alias = tmp.css('#sourceAlias-login::attr(value)').extract_first()

        if not login_csrf_param:
            login_csrf_param = ''

        post_data = {
            'session_key': account,
            'session_password': passwd,
            'isJsEnabled': is_js_enabled,
            'loginCsrfParam': login_csrf_param,
            'sourceAlias': source_alias
        }
        self.logger.info(post_data)
        response = response.replace(url='https://www.linkedin.com/uas/login-submit')
        return scrapy.FormRequest.from_response(response, formdata=post_data, callback=self.after_login,
                                                meta={'cookiejar': response.meta['cookiejar'], 'data': data})

    def after_login(self, response):
        data = response.meta.get('data')
        email = data[2]
        passwd = data[3]
        if 'consumer-email-challenge' in response.url:
            while True:
                code = self.get_vcode(email, passwd, 'pop.163.com')
                time.sleep(2)
                if code:
                    print(code)
                    break
            tmp = response.css('#uas-consumer-ato-pin-challenge')
            sgign = '提交'
            challenge_id = tmp.css('#security-challenge-id-ATOPinChallengeForm::attr(value)').extract_first()
            dts = tmp.css('#dts-ATOPinChallengeForm::attr(value)').extract_first()
            origSourceAlias = tmp.css('#origSourceAlias-ATOPinChallengeForm::attr(value)').extract_first()
            csrfToken = tmp.css('#csrfToken-ATOPinChallengeForm::attr(value)').extract_first()
            sourceAlias = tmp.css('#sourceAlias-ATOPinChallengeForm::attr(value)').extract_first()
            post_data = {
                'PinVerificationForm_pinParam': code,
                'signin': sgign,
                'security-challenge-id': challenge_id,
                'dts': dts,
                'origSourceAlias': origSourceAlias,
                'csrfToken': csrfToken,
                'sourceAlias': sourceAlias,
            }
            self.logger.info(post_data)
            response = response.replace(url='https://www.linkedin.com/uas/ato-pin-challenge-submit')
            yield scrapy.FormRequest.from_response(response, formdata=post_data, callback=self.after_login,
                                                   meta={'cookiejar': response.meta['cookiejar'], 'data': data})
        else:
            yield scrapy.Request(url='http://www.linkedin.com/feed/', callback=self.parse_home,
                                 meta={'cookiejar': response.meta['cookiejar']})

    def parse_home(self, response):
        text = response.text.replace('&quot;', '"')
        res = self.public_id.findall(text)
        self.logger.info(res)
        flag = False

        for one in res[1:]:
            self.logger.info(one)
            flag = True

        if not flag:
            self.logger.warning('Login failed')
        else:
            self.logger.info('Login success')


    def get_vcode(self, mail_user, mail_passwd, mail_host='pop.163.com'):
        # 连接到POP3服务器:
        server = poplib.POP3_SSL(mail_host)
        # 可以打开或关闭调试信息:
        # server.set_debuglevel(1)
        # 可选:打印POP3服务器的欢迎文字:
        # print(server.getwelcome())
        # 身份认证:
        server.user(mail_user)
        server.pass_(mail_passwd)
        # list()返回所有邮件的编号:
        resp, mails, octets = server.list()
        index = len(mails)
        # 收取最新邮件
        resp, lines, octets = server.retr(index)
        msg = '\r\n'.join([one.decode('utf8') for one in lines])
        if 'security' in msg:
            res = re.findall('\s\d{6}\s', msg)[0].strip()
        else:
            res = None
        # 可以根据邮件索引号直接从服务器删除邮件:
        # server.dele(index)
        # 关闭连接:
        server.quit()
        return res


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
