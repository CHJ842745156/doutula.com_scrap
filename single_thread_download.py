# -*- coding:utf-8 -*-

__author__ = 'Mechrevo'

import requests
import re
import random
import time


# 构造存url的列表
url_list = []
for i in range(1,1739):
    url = "http://www.doutula.com/photo/list/?page="
    url_list.append(url+str(i))

# 自己试了爬了几个发现网址有点问题，用这个东西处理一下
def splitEnd(str):
    str = str.split('!dta')[0]
    return str

# 主功能函数
def scrap(url,file,pagenum):

    # 冒充一下浏览器
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

    # 假装用代理反反爬
    proxyList = [{'http':'119.188.162.165:8081'},
             {'http':'203.130.46.108:9090'},
             {'http':'112.126.65.236:80'},
             {'http':'115.28.100.127:80'},
             {'http':'118.190.95.43:9001'},
             {'http':'61.135.217.7:80'}
             ]
    proxyAdd = random.choice(proxyList)

    # 获取页面
    response = requests.get(url,headers=header)


    if(str(response).split('[')[1].split(']')[0]=='200'):

        # 获取html信息
        html = response.text

        # 构造我要的东西的正则
        reg = r'data-original="(.*?)".*?alt="(.*?)"'
        reg = re.compile(reg,re.S)

        # 用正则匹配网页里面所有我要的东西
        imgList = re.findall(reg,html)

        for i in imgList:
            i = list(i)
            i[0] = splitEnd(i[0])
            try:
                line = "[{},{}]\n".format(i[0],i[1])
                file.write(line)
            except Exception as e:
                print(e)
                Logfile = open("D:/python/piyixia_scrap/Log/ScrapLog_SingleLog.txt","a+",encoding="utf-8")
                Logfile.write("[File write in error]"+e+"\n"+"the url is "+url+"\n\n")
                Logfile.close()

        # 看一下进度到哪了
        print("have download href for "+str(pagenum)+"/1738 pages")
        time.sleep(1)
    else:
        Logfile = open("D:/python/piyixia_scrap/Log/ScrapLog_SingleLog.txt","a+",encoding="utf-8")
        Logfile.write("[Connection Error]"+"error code:"+str(response).split('[')[1].split(']')[0]+" the url is "+url+"\n"
                      +"the proxy address is:"+str(proxyAdd)+"\n"+"\n")
        Logfile.close()



for i in range(1,1739):
    try:
        file = open("D:/python/piyixia_scrap/meme_single_thread.txt","a+",encoding="utf-8")
    except Exception as e:
        print(e)
    else:
        scrap(url_list[i-1],file,i)
        file.close()