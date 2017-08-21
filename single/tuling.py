# -*- coding:utf-8 -*-
import requests
import re


class Tuling:
    def __init__(self):
        self.timeout = 5

    def get_reply(self, msg):
        url = 'http://www.tuling123.com/openapi/api?key=4095fab195ee4ccdb4a62a70fab83e79&info={0}'.format(msg)
        try:
            r = requests.get(url, timeout=self.timeout)
        except:
            return None
        reply = re.findall(r'"text":"(.*?)"}', r.text)[0]
        return reply

if __name__ == '__main__':
    a = Tuling()
    reply = a.get_reply('你的名字是什么')
    print reply
