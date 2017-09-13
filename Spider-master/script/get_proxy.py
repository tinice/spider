"""
Usage:
  proxy.py target <target> run_times <run_times> [--threadhold=<threadhold>] [--cycle_time=<cycle_time>] [--timeout=<timeout>] [--process_num=<process_num>] [--thread_num=<thread_num>]
  proxy.py clean <clean>
  proxy.py --length
  proxy.py (-h | --help)
  proxy.py --version

Options:
  -h --help                     Show this screen.
  --version                     Show version.
  --threadhold=<threadhold>     Set the threadhold value ,ensure at least  num proxies avaliable [default: 10].
  --cycle_time=<cycle_time>     Set cycle time,every cycle_time seconds to check db [default: 60].
  --timeout=<timeout>           Set proxy timeout value [default: 5].
  --process_num=<process_num>   Set process num [default: 2].
  --thread_num=<thread_num>     Set thread num  [default: 25].
  --length                      Show DB proxies num
"""

from validate import Validator
import requests
import pymongo
import time
from docopt import docopt


class Proxy(object):

    def __init__(self,target,run_times,threadhold,cycle_time,timeout,thread_num,process_num):
        self.client = pymongo.MongoClient('mongodb://poluo:poluo123@115.28.36.253:27017/proxy')
        self.db = self.client.proxy
        self.collection = self.db.proxy_list
        self.validate = Validator(target,timeout,process_num,thread_num)
        self.run_count = run_times
        self.threadhold = threadhold
        self.cycle_time = cycle_time #seconds

    def get_proxy(self,num):
            tid = '555947027942665'
            url = 'http://tvp.daxiangdaili.com/ip/?tid={}&num={}&category=2&delay=5&protocol=https&ports=80,8080,3128'.format(tid, num)
            ip_all = []
            result = requests.get(url)
            result = result.text.split('\n')
            for one in result:
                if one != '':
                    ip = {
                        'ip': one.split(':')[0].strip(),
                        'port': one.split(':')[1].strip()
                    }
                    ip_all.append(ip)
            if len(ip_all) == 0:
                print('NO PROXY AVAILABLE')
            else:
                print('update proxy')
            return ip_all

    def insert(self,result):
        for i in result:
            self.collection.insert(i)
            print(i) 
    def get_length(self):
        count = 0
        for one in self.collection.find():
            count += 1
        return count
        
    def check_db(self):
        ip_all=[]
        for one in self.collection.find():
            ip_all.append(one)
            self.collection.remove(one)
        tmp = self.validate.run(ip_all)
        ip_all = []
        for one in tmp:
            if one['speed'] < 10:
                ip_all.append(one)
        if len(ip_all):
            print('check db:')
            self.insert(ip_all)
        
        
    def run(self,num):
        while self.run_count:
            if self.run_count%2==0:
                self.check_db()
            print('Run times count {}'.format(self.run_count))
            self.run_count -= 1
            start = time.time()
            while self.get_length() < self.threadhold:
                ip_all = self.get_proxy(num)
                tmp=self.validate.run(ip_all)
                ip_all = []
                for one in tmp:
                    if one['speed'] <10:
                        ip_all.append(one)
                if len(ip_all):
                    self.insert(ip_all)
                    break
                else:
                    print('no valid')
            print('proxies num in db {}'.format(self.get_length()))
            if self.run_count:
                print('Already satisfied the setting,sleep....')
                time.sleep(self.cycle_time-(time.time()-start))
            else:
                print('Run time finished, quit.')


def clean_db():
    client = pymongo.MongoClient('mongodb://poluo:poluo123@115.28.36.253:27017/proxy')
    db = client.proxy
    collection = db.douban_movie2
    for one in collection.find():
        collection.remove(one)
    print('clean db finished')
def show_length():
    client = pymongo.MongoClient('mongodb://poluo:poluo123@115.28.36.253:27017/proxy')
    db = client.proxy
    collection = db.douban_movie2
    
    length=len(list(collection.find()))
    print('length {}'.format(length))
    collection = db.douban_actress
    length=len(list(collection.find()))
    print('actress length {}'.format(length)) 
if __name__ == '__main__':
    arguments = docopt(__doc__,version = '1.0.0')
    #print('Your argments is {}'.format(arguments))
    length_flag = arguments['--length']
    clean_flag = arguments['<clean>']
    if length_flag:
        show_length()
    elif clean_flag:
        clean_db()
    else:
        target = arguments['<target>']
        run_times = int(arguments['<run_times>'])
        threadhold = int(arguments['--threadhold'])
        cycle_time = int(arguments['--cycle_time'])
        timeout = int(arguments['--timeout'])
        thread_num = int(arguments['--thread_num'])
        process_num = int(arguments['--process_num'])
        my_proxy=Proxy(target,run_times,threadhold,cycle_time,timeout,thread_num,process_num)
        my_proxy.run(50)
