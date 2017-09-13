from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import multiprocessing
import json


# path="C:\Program Files (x86)\Google\Chrome\chromedriver"
# driver = webdriver.Chrome(executable_path=path)

cap = webdriver.DesiredCapabilities.PHANTOMJS
cap["phantomjs.page.settings.resourceTimeout"] = 1000
cap["phantomjs.page.settings.loadImages"] = False
cap["phantomjs.page.settings.disk-cache"] = True

#driver=webdriver.PhantomJS(desired_capabilities=cap)
def get_detail_info(offset):
    '''get netease music playlist info'''
    base_url="http://music.163.com"
    url=base_url+offset
    result = []
    driver.get(url)
    print(driver.title)
    driver.switch_to_frame("g_iframe")

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#song-list-pre-cache > div > div > table > tbody > tr"))
    )
    
    element = driver.find_elements_by_css_selector("#song-list-pre-cache > div > div > table > tbody > tr")
    for one in element:
        try:
            data={
            'song_id':one.find_elements_by_css_selector("span.txt > a")[0].get_attribute('href'),
            'song_name':one.find_elements_by_css_selector("span.txt > a")[0].text,
            'song_length':one.find_elements_by_css_selector("span.u-dur")[0].text,
            'singer_name':one.find_elements_by_css_selector("td:nth-child(4) > div > span > a")[0].text,
            'singer_id':one.find_elements_by_css_selector("td:nth-child(4) > div > span > a")[0].get_attribute('href'),
            'album_name':one.find_elements_by_css_selector("td:nth-child(5) > div > a")[0].text,
            'album_id':one.find_elements_by_css_selector("td:nth-child(5) > div > a")[0].get_attribute('href')
            }
            result.append(data)
        except Exception as e:
            print("{0} occur error {1}".format(data,e))
    
    with open('{0}.json'.format(offset[offset.find('=')+1:]),'w') as fobj:
            json.dump(result,fobj)
    print("{0} is fininsh\n".format(offset))

def grasp_main():
    count = 11
    tmp =0 
    while count:
        with open("result{0}.json".format(count),'r')  as fobj:
            data_list = json.load(fobj)
        print(len(data_list))
        count = count -1
        pool= multiprocessing.Pool()
        for data in data_list:
            pool.apply_async(get_detail_info, args=(data['href'],))
        pool.close()
        pool.join()
        break
        time.sleep(20)
if __name__ == '__main__':
    start = time.time()
    #mymusic=NeteaseMusic()
    grasp_main()

    end = time.time()
    print(end-start)
