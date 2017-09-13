"""
Usage:
  check.py target <target> [--timeout=<seconds>] process <process_num> thread <thread_num>
  check.py (-h | --help)
  check.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import logging
import sys
from pymongo import MongoClient
import json
from validate import Validator
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
from docopt import docopt

def clean():
    logging.info('start clean')
    client = MongoClient('mongodb://poluo:poluo123@127.0.0.1:27017/proxy')
    db = client.proxy
    collection = db.proxy_list
    for one in collection.find():
        collection.remove(one)
    logging.info('db clean finish')
def db(result):
    logging.info('start insert')
    client = MongoClient('mongodb://poluo:poluo123@127.0.0.1:27017/proxy')
    db = client.proxy
    collection = db.proxy_list
    for one in result:
        collection.insert(one)
    logging.info('db insert finish')

def main():
    arguments = docopt(__doc__,version = '1.0.0')
    target = arguments['<target>']
    timeout = int(arguments['--timeout'])
    thread_num = int(arguments['<thread_num>'])
    process_num = int(arguments['<process_num>'])
    print('{} {} {} {}'.format(target,timeout,thread_num,process_num))
    validator = Validator(target,timeout,process_num,thread_num)
    ip_all=[]
    logging.info("Load proxy ip, total: %s", len(ip_all))
    result_tmp = validator.run(ip_all)
    result=[]
    for one in result_tmp:
        if one["speed"] > 8:
            pass
        else:
            result.append(one)
    logging.info("validator run finished")
    logging.info(len(result))
    result = sorted(result, key=lambda x: x["speed"])
    return  result

if __name__ == '__main__':
    main()
