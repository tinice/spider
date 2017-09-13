import gevent
import time
from urllib.request import urlretrieve
from multiprocessing import Process
from functools import wraps
from gevent import monkey
monkey.patch_all()


THREAD_NUM = 20
PROCESS_NUM = 4


def multi_process(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url,start,end = args
        piece = (end-start)//PROCESS_NUM
        process_list = []
        for _ in range(PROCESS_NUM):
            process = Process(target=func, args=(url,start,start+piece))
            process_list.append(process)
            process.start()
            start += piece

        for process in process_list:
            process.join()
    return wrapper


def multi_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url,start,end  = args
        jobs= []
        piece = (end-start)//THREAD_NUM
        for _ in range(THREAD_NUM):
            jobs.append(gevent.spawn(func,url,start,start+piece))
            start += piece
        gevent.joinall(jobs)
        # get  return value
        # result = []
        # for j in jobs:
        #     result.append(j.value)
        # return result
    return wrapper

@multi_process
@multi_thread
def demo(url,start,end):
    while start <= end:
        urlretrieve(url, './zhihu/img_{}.jpg'.format(int(start)))
        start += 1

if __name__ == '__main__':
    url = 'https://www.zhihu.com/captcha.gif?r=1495023104578&type=login'
    start = time.time()
    demo(url,1,1000)
    print('takes {} s'.format(time.time()-start))

