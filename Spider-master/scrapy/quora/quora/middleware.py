import logging as log
import os
import requests
import time
from scrapy.exceptions import IgnoreRequest


class CustomNormalMiddleware(object):
    def __init__(self):
        self.frmdata = {}
        self.frmdata['json'] = '{"args":[],"kwargs":{"email":"997786818@qq.com","password":"poluo123"}}'
        self.frmdata['formkey'] = '75ec5150317eefe0dae46fc9f101a5da'
        self.frmdata['postkey'] = 'fc42a7c6aeffd2a56634a5e750b312a4'
        self.frmdata['window_id'] = 'dep3200-335053055489061942'
        self.frmdata['referring_controller'] = 'index'
        self.frmdata['referring_action'] = 'index'
        self.frmdata['__vcon_json'] = '["Vn03YsuKFZvHV9"]'
        self.frmdata['__vcon_method'] = 'do_login'
        self.frmdata['__e2e_action_id'] = 'eojq4wgqa9'
        self.frmdata['js_init'] = '{}'
        self.frmdata['__metadata'] = '{}'
        self.cookies = {'m-b': 'pGLDg-FVmqrI6CF2993g9g\075\075', 'm-s': 'asXhk8Af26gYfG5n-beTXw\075\075',
                        'm-css_v': 'ec931eb5703b888f',
                        'm-login': '0', 'm-early_v': '0f20c735abd3a97d', 'm-tz': '-480',
                        'm-wf-loaded': 'q-icons-q_serif',
                        '_ga': 'GA1.2.420550872.1490615030'}
        self.login_count = 0

    def process_request(self, request, spider):
        request.meta['count'] = self.login_count

    def process_response(self, request, response, spider):
        if response.status == 429:
            try:
                count = request.meta['count']
            except AttributeError as e:
                log.info('request no meta count {}'.format(e))
                count = self.login_count
            log.info('login count = {}'.format(self.login_count))
            log.info('count = {}'.format(count))
            if count == self.login_count:
                self.login_count += 1
                log.info('429 retry login')
                cmd_str = "adsl-stop"
                os.system(cmd_str)
                time.sleep(0.1)
                cmd_str = "adsl-start"
                os.system(cmd_str)
                time.sleep(0.2)
                tmp = requests.post('https://www.quora.com/webnode2/server_call_POST', data=self.frmdata,
                                    cookies=self.cookies)
                if tmp.status_code == 200:
                    log.info('retry login,post success')
                else:
                    log.info('retry login,post failed')
            return response
        else:
            return response
