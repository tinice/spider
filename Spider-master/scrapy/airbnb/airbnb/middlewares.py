import logging as log


class CustomNormalMiddleware(object):
    def __init__(self):
        self.cookies = {
            '_csrf_token': 'V4%24.airbnb.com%24Wdz9n2RJ8ms%24RslB7et3ZmxOD6H5w7lM8X0pBudHRqPxahfNuENZb18%3D',
            '_user_attributes': '%7B%22curr%22%3A%22CNY%22%2C%22guest_exchange%22%3A6.89531%2C%22device_profiling_session_id%22%3A%221493599251--327a7add54552be2c4cd462a%22%2C%22giftcard_profiling_session_id%22%3A%221493599251--d7075c1df818efa8a01fb9cf%22%2C%22reservation_profiling_session_id%22%3A%221493599251--1c16a10b8f7a862f31a98f36%22%7D',
            'flags': '268435456', 'p1_hcopy6': 'control', 'mdr_browser': 'desktop', 'sdid': '', 'ftv': '1493599243563',
            '__ssid': 'bd0bbeaf-635e-4b8d-b07a-7ee637152907', '__ag_cm_': '1', 'ag_fid': 'g2975NOPaUVsMSHF',
            'EPISODES': 's', '_ga': 'GA1.2.1367190750.1493599243', 'bev': '1493599251_yf9qwW0YTaCYpSEE'}

    def process_request(self, request, spider):
        request.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        request.headers[
            'Accept'] = 'application/json, text/javascript, */*; q=0.01'
        request.headers['Accept-Encoding'] = 'gzip, deflate, sdch, br'
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        request.headers['Connection'] = 'keep-alive'
        request.headers['referer'] = 'https://zh.airbnb.com/'
        request.headers['dnt'] = 1
        request.headers['x-csrf-token'] = 'V4$.airbnb.com$Wdz9n2RJ8ms$RslB7et3ZmxOD6H5w7lM8X0pBudHRqPxahfNuENZb18='
        request.headers['x-requested-with'] = 'XMLHttpRequest'
        try:
            cookies_enable = request.meta.get('cookies')
        except Exception as e:
            log.info(e)
            cookies_enable = True
        if cookies_enable:
            try:
                self.cookies[':authority'] = 'zh.airbnb.com'
                self.cookies[':method'] = 'POST'
                self.cookies[':path'] = request.meta.get('path')
                self.cookies[':scheme'] = 'https'
            except Exception as e:
                log.info(e)
                self.cookies[':authority'] = 'www.jd.com'
                self.cookies[':method'] = 'GET'
                self.cookies[':path'] = '/'
                self.cookies[':scheme'] = 'https'
            request.cookies = self.cookies
