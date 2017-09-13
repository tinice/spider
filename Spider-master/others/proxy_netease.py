import requests
import json


class Proxy(object):
    """docstring for Proxy"""
    def __init__(self):
        self.pending = []
        	
    def get_proxy(self):
        orginal_url="http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10"
        web=requests.get(orginal_url)
        web.encoding='utf-8'
        info=json.loads(web.text)
        info=info['rows']
        for one in info:
            data={
            'ip':one['ip'],
            'port':one['port'],
            'anony':one['anony'],
            'type':one['type'],
            }
            self.pending.append(data)

        with open('proxy.json','w') as fobj:
        	json.dump(self.pending,fobj)

        self.pending=[]
     
if __name__ == '__main__':

    test=Proxy()
    test.get_proxy()
