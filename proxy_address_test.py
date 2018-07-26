__author__ = 'Mechrevo'


import requests
from urllib import request
import random

proxyList = [{'http':'119.188.162.165:8081'},
             {'http':'112.126.65.236:80'},
             {'http':'115.28.100.127:80'},
             {'http':'118.190.95.43:9001'},
             {'http':'61.135.217.7:80'}
             ]
for i in proxyList:
    proxyAdd = i
    px = request.ProxyHandler(proxyAdd)

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

    url = "http://www.doutula.com/photo/list/?page=3"

    try:
        response = requests.get(url,proxies=proxyAdd,headers=header)
        print(response," ",proxyAdd)
    except Exception as e:
        print(e," ",proxyAdd)