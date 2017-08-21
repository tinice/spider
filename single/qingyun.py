# -*- coding:utf-8 -*-
import requests
import re


class Qingyun:
    def __init__(self):
        self.timeout = 5

    def get_reply(self, msg):
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg=={0}'.format(msg)
        try:
            r = requests.get(url, timeout=self.timeout)
        except:
            return None
        reply = re.findall(r'"content":"(.*?)"}', r.text)[0]
        return reply

if __name__ == '__main__':
    a = Qingyun()
    reply = a.get_reply('会唱歌吗')
    print reply

