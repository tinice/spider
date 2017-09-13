import multiprocessing
import gevent
from gevent import monkey
import urllib
monkey.patch_all()


class Downloader:

    def __init__(self, procs_num,thread_num):
        self._procs_num = procs_num
        self._thread_num = thread_num
        logging.info("Init Downloader...\n  process num: %s\nthread num: %s", procs_num, thread_num)

    def run(self, url,start,end):
        result_queue = multiprocessing.Queue()
        piece = (end-start)//self._procs_num
        process = []
        for i in range(self._procs_num):
            p = multiprocessing.Process(target=self.process_with_gevent, args=(result_queue,start,start+piece,url))
            start += piece
            process.append(p)
            p.start()
        
        for p in process:
            p.join(10)

        result = []
        for p in process:
            result.extend(result_queue.get())
        return result

    def process_with_gevent(self,result_queue,start,end,url):
        jobs = []
        piece = (end-start)//self._thread_num

        for _ in range(self._thread_num):
            jobs.append(gevent.spawn(self.worker,[start,start+piece,url]))
            start += piece

        gevent.joinall(jobs)
        result = []
        for j in jobs:
            result.extend(j.value)

        result_queue.put(result)

    def worker(self,num):
        start,end=num[0],num[1]
        url = num[2]
        self.download(url,start,end)
        return 0

    def download(self, url, start,end):
        count = start
        while count < end:
            count += 1
            print(count)
            urllib.request.urlretrieve(url, './zhihu/img_{}.jpg'.format(count))

if __name__ == '__main__':
    url = 'https://www.zhihu.com/captcha.gif?r=1495023104578&type=login'
    my_downloader = Downloader(2,5)
    my_downloader.run(url,1000,8000)
        
