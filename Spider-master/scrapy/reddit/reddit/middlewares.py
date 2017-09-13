import logging as log


class CustomNormalMiddleware(object):
    def __init__(self):
        self.cookies = {
            'loid': '000000000000hriw49.2.1494119331045.Z0FBQUFBQlpEbk9qMmlvN1JzVnM5enlETWh5UnZKbkVUYXp4UEZQcmRTV3JITWJwSG03ZHNWVTdMc1NmWnpTTm5fOUhPMlJrS2ZuVS1aRktpeUxGZl82N0E3by1LOC1oZTJMeXFldnoxMUw0RzBTNnJ1LWRoWTYxU0tWRExYWmMtQUQyaUxVbW5RV3A',
            'edgebucket': 'JTUNPEO4EfmPguPZMx',
            '_recent_srs': 't5_2r0ij%2Ct5_2qh13%2Ct5_38unr%2Ct5_2qh1i%2Ct5_2qh33%2Ct5_2rp0g%2Ct5_2wbww',
            'session_tracker': 'GqNF2BCXyMe8DMaoED.0.1494158608743.Z0FBQUFBQlpEdzBROWFRa3dLZ0RNYkNObmZhSkxrVFVDMXhoZHFuTGxTOVdzeXN3ZG03bmpRX1d2aEFzaDhIWnJYRF8zcDNLNEdHQnVvbmZRWDdjZS1SVnhlMW1tak54d2ZWa1h2Ry1NYThwNzhUSTZ4NlVRclJIRUlEMHF3bk1GcVBMcHM3REtZckw',
            'pc': 'zz'}

    def process_request(self, request, spider):
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        request.headers[
            'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8'
        request.headers['Connection'] = 'keep-alive'
        request.headers['upgrade-insecure-requests'] = 1
        request.headers['dnt'] = 1
        try:
            cookies_enable = request.meta.get('cookies')
        except Exception as e:
            log.info(e)
            cookies_enable = True
        if cookies_enable:
            try:
                self.cookies[':authority'] = 'www.reddit.com'
                self.cookies[':method'] = 'GET'
                self.cookies[':path'] = request.meta.get('path')
                self.cookies[':scheme'] = 'https'
            except Exception as e:
                log.info(e)
                self.cookies[':authority'] = 'www.reddit.com'
                self.cookies[':method'] = 'GET'
                self.cookies[':path'] = '/subreddits'
                self.cookies[':scheme'] = 'https'
            request.cookies = self.cookies
