from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests as r
import json
import time
import os
# 記得要到chrome上載入xpath-helper_v2.0.2.crx
# https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl




#input: str
#output: list
def selenium_start(search_url, keyword):
    #find path of chrome.exe, chromedriver.exe
    Options.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    webdriver_path = './chromedriver.exe'


    driver = webdriver.Chrome(executable_path=webdriver_path)
    driver.maximize_window()

    driver.get(search_url)

    # find search lacation
    search_input = driver.find_element_by_name('p')
    search_input.send_keys(keyword)

    # click button
    start_search_btn = driver.find_element_by_class_name('ygbt')
    start_search_btn.click()

    for i in range(1000):
        try:
            start_more_pic = driver.find_element_by_name('more-res')
            start_more_pic.click()

            # scroll to buttom step by 100
            driver.execute_script('var q=document.documentElement.scrollTop=' + i * 100)
            time.sleep(3)

        except:
            pass

    htmltext = driver.page_source
    soup = BeautifulSoup(htmltext, "html.parser")
    img_html = soup.select('img[src]')


    # k = 0
    # for i in img_html:
    #     k+=1
    # # appear number of data
    # # every url of pic appears 2 times
    # print(k / 2)


    return img_html



#input: list of img_html
#output: list of img_src
def split_html(img_html):
    list_src = []
    for i in img_html:
        src = i.get('src')
        list_src.append(src)

    return list_src



#input: list of src
#output: list of index
def get_index(src_list):
    index_list = []
    for i in src_list:
        index = str(i).split('?')[1].split('&')[0].split('=')[1]
        index_list.append(index)

    return index_list


#input: list
#output: dict
def get_dict(index_list, src_list):
    dict_src = dict(zip(index_list, src_list))

    return dict_src





def download_pic(index,src):
    if not os.path.exists('./project_photos'):
        os.mkdir('./project_photos')
    img_data = r.get(src).content
    with open("project_photos/" + str(index + 1) +'.jpg', 'wb+') as f:
        f.write(img_data)







def main():
    src_list =[]
    index_list = []
    search_url = 'https://tw.images.search.yahoo.com/images'
    # 'headshot female','生活照','男證件照''女證件照','headshot male','life photo','大頭照','mug shot','家庭照','大合照','family portrait','側面照','被面照',' side view','back view'
    keyword = ['沙龍照','Salon photo']

    for i in keyword:
        img_html = selenium_start(search_url,i)
        src_list = src_list + split_html(img_html)
        index_list = index_list + get_index(src_list)

    src_dict = get_dict(index_list, src_list)

    src_list = list(src_dict.values())

    for index, src in enumerate(src_list):
        download_pic(index, src)








if __name__ == '__main__':

    main()