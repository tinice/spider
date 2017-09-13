import requests
import json
from furl import furl

class Demo(object):
    """docstring for Proxy"""
    def __init__(self):
        self.pending = []
        self.headers={'User-Agent':'AiMovie /OnePlus-7.0-OnePlus3-1920x1080-480-7.9.1-7911-860046034572018-Oppo',
                    'Accept-Encoding':'gzip',
                    'Connection':'Keep-Alive',
                    'Host':'api.maoyan.com'}
        	
    def run(self):
        for one in range(10):
            f = furl('http://api.maoyan.com/mmdb/search/movie/tag/list.json?')
            arg = {'cityId': '30', 'limit': '10', 'offset': str(one*10),
                   'catId': '-1', 'sourceId': '-1', 'yearId': '1',
                   'sortId': '3', 'token': '', 'utm_campaign': 'AmovieBmovieCD-1',
                   'movieBundleVersion':'7911','utm_source':'Oppo','utm_medium':'android','utm_term':'7.9.1',
                   'utm_content':'860046034572018','ci':'30','net':'255','dModel':'ONEPLUS%20A3000', 
                   'uuid':'3957877BBCA515101B23ABC3B14C92D2364184F6E53440B4AC51D7A07F1A66C0',
                   'lat':'22.517843','lng':'113.927976',
                   '__reqTraceID':'-5540599105416656096',
                   'refer':'%2FMovieMainActivity','__skck':'6a375bce8c66a0dc293860dfa83833ef',
                   '__skts':'1494507036905','__skua':'32bcf146c756ecefe7535b95816908e3',
                   '__skno':'a9f816b9-6001-4144-adbf-d327a08c81e4','__skcy':'Ew855TygVhpqeAfOl0C3ObUq4u8'}
            f.add(args=arg)
            orginal_url=f.url
            web=requests.get(orginal_url,headers=self.headers)
            print(web.text)
        
     
if __name__ == '__main__':

    test=Demo()
    test.run()
