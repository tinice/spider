import logging as logger


class CustomNormalMiddleware(object):
    def __init__(self):
        res ={}
        with open('C:/Users/poluo/PycharmProjects/tmall/tmall/cookies.txt', 'r') as fobj:
            for line in fobj:
                tmp = line.split(';')
                for one in tmp:
                    index = one.index('=')
                    res[one[:index].strip()] = one[index + 1:].replace('\"', '')
            logger.info(res)
        self.cookies = res

    def process_request(self, request, spider):
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = 'www.tmall.com'
        request.headers['cache-control'] = 'max-age=0'
        request.headers['upgrade-insecure-requests'] = 1
        request.headers['DNT'] = 1
        try:
            headers_enable = request.meta.get('headers')
        except Exception as e:
            logger.info(e)
            headers_enable = False
        if headers_enable:
            try:
                request.headers['Host'] = request.meta.get('Host')
            except Exception as e:
                logger.info(e)

        if self.cookies:
            request.cookies = self.cookies

    def process_response(self, request, response, spider):
        if response.status != 200:
            logger.warning('response status not 200 {}'.format(response.url))
            return response
        else:
            return response

