#!/bin/env python
# -*- coding:utf-8 -*-

import requests
import time


class Xiaobing:
    def __init__(self):
        self.cookie = 'SCF=Avij6Khf1BkvuDp5rOxhQPTN4JmraGIJfy68uT6PT2gmZEeoQH3VthSnVEiZD8NjjWmz3HwapuL5NSPwTjTPnYs.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWeP1M_d5p8IWBO1a4HxSkm5JpX5o2p5NHD95Q0SoeNehe4SoefWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNe0q0S0501Kq0SBtt; _T_WM=4e2ebab8ade3864f3a99988d6b9998e0; SUB=_2A250T1HEDeRhGeVI6FUR8yfKyDmIHXVXsH-MrDV6PUJbkdANLWjWkW2XyMXLVGtrtwyDBJJwdYxwUVdK_w..; SUHB=08J7QtVSowwwIL; SSOLoginState=1498096020'
        self.header = {
            'Cookie': self.cookie
        }
        self.send_url = 'https://weibo.cn/msg/do/post?st=4947db'
        self.reply_url = 'https://m.weibo.cn/msg/messages?uid=5175429989'
        self.timeout = 5

    def send(self, msg):
        body = {
            'content': msg,
            'rl': 2,
            'uid': '5175429989',
            'send': u'发送'
        }
        try:
            responses = requests.post(self.send_url, data=body, headers=self.header, timeout=self.timeout, verify=False)
        except:
            return 'send requests fail'

    def receive(self, msg):
        send_result = self.send(msg)
        if send_result == 'send requests fail':
            return send_result
        time.sleep(2)
        start = time.time()
        try:
            responses = requests.get(self.reply_url, headers=self.header, timeout=self.timeout, verify=False)
        except:
            return 'reply requests fail'
        result = responses.json()
        reply = result['data'][0]['text']
        all_time = time.time() - start
        if u'分享图片' in reply:
            return 'reply is picture'
        if u'分享语音' in reply:
            return 'reply is voice'
        if reply == msg:
            return 'no_reply'
        print all_time
        return reply

if __name__ == '__main__':
    a = Xiaobing()
    info_list = ['来张图片', '微笑', 'hello', 'sorry', '好想哭啊']
    for i in info_list:
        print a.receive(i)
