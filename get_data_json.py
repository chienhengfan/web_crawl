# coding=gbk
from datetime import date
from multiprocessing import Pool,managers
import crowler104
import os
import json
import time


def getlist():
    if not os.path.exists('./data'):
        os.mkdir('./data')
    else:
        pass
    list = catch()['index']
    print(len(list))
    print("please wait...")
    for i in os.listdir('./data/'):
        if i.strip('.json') in list:
            #del list[list.index(i.strip('.json'))]
            list.remove(i.strip('.json'))
    print("got catching list!!",list)
    print(len(list))
    return list

def catch():

    cachefilename = crowler104.cachefilename().name  #�n�����Q�鮔������
    #cachefilename = './2020-08-26.json'               #�̶��n�����Q
    cachedict = crowler104.open_json_file(cachefilename)
    return cachedict

def cach_to_json(index):
    if len(index) <10:
        url = "https://www.104.com.tw/job/ajax/content/"+index
        try:
            j = crowler104.extract(index,crowler104.crowl(url))
            crowler104.write_json('./data/{}.json'.format(index), j)
        except Exception as e:
            print("error:",e)
            time.sleep(2)
    else:
        pass




if __name__ == '__main__':

    list = getlist()
    print(list)
    p = Pool(8)

    p.map(cach_to_json,iterable=(i for i in list))

    p.close()
    p.join()

    #crowler104.write_json('./final.json',d)
