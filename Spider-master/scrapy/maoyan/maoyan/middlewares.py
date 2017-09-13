class CustomNormalMiddleware(object):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = 'AiMovie /OnePlus-7.0-OnePlus3-1920x1080-480-7.9.1-7911-860046034572018-Oppo'
        request.headers['Accept-Encoding'] = 'gzip'
        request.headers['Connection'] = 'keep-alive'
        request.headers['Host'] = 'api.maoyan.com'
