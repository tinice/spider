# -*- coding:utf-8 -*-
import os
import re
import threadpool
import time
import requests


def water(kw_url):
    respones = requests.get(kw_url)
    info = respones.content
    sn = re.findall(r'sn":"(.*?)","qid', info)
    result_list = []
    for i in sn:
        new_url = 'https://live2.jia.360.cn/public/getLiveList?src=test_jia_360&sn=' + i
        respones2 = requests.get(new_url)
        online = re.findall(r'online":"(.*?)","status', str(respones2.content))[0]
        rtmp = re.findall(r'_LC(.*?)","hls', str(respones2.content))[0]
        new_rtmp = 'rtmp://rlive.jia.360.cn/live_jia_public/_LC' + rtmp
        result = {}
        result["online"] = online
        result["rtmp"] = new_rtmp
        result_list.append(result)
    return result_list


def get_video(command):
    os.system(command)
    time.sleep(3)


if __name__ == '__main__':
    result_list = []
    for i in range(4):
        url = 'https://live2.jia.360.cn/public/getPublicListByTag?isPage={0}&sortType=1&callback=jQuery110209844467151055092_1496718615446&orderBy=&count=16&from=mpc_ipcam_web&category=4&tag=52&page=0&_=1496718615449'.format(i)
        result = water(url)
        result_list.extend(result)
    command_list = []
    for h in result_list[0:4]:
        command = 'ffmpeg -t 20 -i ' + h["rtmp"] + ' -c copy ' + h["rtmp"][-11:] + '.flv'
        command_list.append(command)
    pool = threadpool.ThreadPool(5)
    requestss = threadpool.makeRequests(get_video, command_list)
    [pool.putRequest(req) for req in requestss]
    pool.wait()
    # print result_list
    # result_dict = {}
    # result_dict["data"] = result_list
    # with open('result.json', 'w') as f:
    #     f.write(json.dumps(result_dict))
