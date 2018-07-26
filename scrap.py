# -*- coding:utf8 -*-

__author__ = 'Mechrevo'

import requests
import urllib.request as ur
import re
import random
import time
import threading

# 设定一个记录爬取页面数量的量
pagenum = 0
lock = threading.Lock()

# 图片信息总表
imgCollection = []

# 给pagenum加锁
def addPageNum():
    global pagenum
    lock.acquire()
    temp = pagenum
    pagenum = temp + 1
    lock.release()

# 给imgCollection加锁
def imglistAppend(imgList):
    global imgCollection
    lock.acquire()
    temp = imgList
    imgCollection.append(temp)
    lock.release()

# 原来收下来的图片url有点问题，修一下
def splitEnd(str):
    str = str.split('!dta')[0]
    return str

# 构造爬取主功能
def scrap(url):
    # 假冒浏览器
    UA_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400"]
    headStr = random.choice(UA_list)
    header = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
              "Connection":"keep-alive",
              "User-Agent":headStr}

    #代理设置
    proxyList = [{'http':'119.188.162.165:8081'},
             {'http':'112.126.65.236:80'},
             {'http':'115.28.100.127:80'},
             ]
    proxyAdd = random.choice(proxyList)

    try:
        # 构造页面请求
        response = requests.get(url_list[1],proxies=proxyAdd,headers=header)
    except Exception as e:
        print(e)
        Logfile = open("D:/python/piyixia_scrap/Log/ScrapLog.txt","a+",encoding="utf-8")
        Logfile.write("[Response Error]"+str(e)+" the url is "+url+"\n"
                      +"the proxy address is:"+str(proxyAdd)+"\n"+"\n")
        Logfile.close()

    if(str(response).split('[')[1].split(']')[0]=='200'):
        # 获取html信息
        html = response.text

        # 构造我要的东西的正则
        reg = r'data-original="(.*?)".*?alt="(.*?)"'
        reg = re.compile(reg,re.S)

        # 用正则匹配网页里面所有我要的东西
        imgList = re.findall(reg,html)

        try:
            imglistAppend(imgList)
        except Exception as e:
            print(e)
        else:
            addPageNum()
            print("have download href for "+str(pagenum)+"/1738 pages")

        time.sleep(1)
    else:
        Logfile = open("D:/python/piyixia_scrap/Log/ScrapLog.txt","a+",encoding="utf-8")
        Logfile.write("[Connection Error]"+"error code:"+str(response).split('[')[1].split(']')[0]+" the url is "+url+"\n"
                      +"the proxy address is:"+proxyAdd+"\n"+"\n")
        Logfile.close()








def writeUrlIntoFile(imgCollection):
    try:
        file = open("D:/python/piyixia_scrap/meme.txt","a+",encoding="utf-8")
    except Exception as e:
        print(e)
    else:
        for i in imgCollection:
            i = list(i)
            i[0] = splitEnd(i[0])
            try:
                line = "[{},{}]\n".format(i[0],i[1])
                file.write(line)
            except Exception as e:
                print(e)
            else:
                file.close()



#构造url列表
url_list = []
for i in range(1,1739):
    url = "http://www.doutula.com/photo/list/?page="
    url_list.append(url+str(i))


class myThread(threading.Thread):
    def __init__(self,startPage,endPage):
        threading.Thread.__init__(self)
        self.startPage = startPage
        self.endPage = endPage

    def run(self):
        for i in range(self.startPage,self.endPage+1):
            scrap(url_list[i-1])


threads = []

thread1 = myThread(1,580)
thread2 = myThread(581,1060)
thread3 = myThread(1061,1738)

thread1.start()
thread2.start()
thread3.start()

threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

for t in threads:
    t.join()

writeUrlIntoFile(imgCollection)

