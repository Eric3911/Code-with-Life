# coding=utf-8
'''
#该脚本的功能爬去数据库的图片数据(谷歌浏览器)
    1、载入数据地址
    2、修改Host
    3、修改存储文件路径
'''
import urllib.request
import urllib3
from time import strftime, sleep
import requests
import json
import time

from bs4 import BeautifulSoup

#分析页面
def getUrl(urls):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Cookie': 'JSESSIONID=F56829C344F5270ABE238F9EBF6DB62A',
               'Host': '121.201.83.194:8040',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
               }

    # cookies = {
    # }
    resultPage = requests.get(urls, headers=headers)  # 在请求中设定头，cookie
    soup = BeautifulSoup(resultPage.text)  # 实例化一个BeautifulSoup对象
    scrr = soup.findAll('p')
    lst = scrr[0].text[1:][:-1].split(",{")
    imgLst = []
    for tab in lst:
        print(tab)
        if not str(tab).startswith("{"):

            tab = "{"+tab
        d1 = eval(tab)
        if d1["cameraNo"] == 1:
           # print(d1["imgUrl"])
            imgLst.append(d1["imgUrl"])
    for img in imgLst:
        print(img)
        try:
            urllib.request.urlretrieve(img, 'E:/code with life/3/%s.jpg' % int(round(time.time() * 1000)))  #图片存入路径
        except urllib.error.HTTPError:
            continue
    print("over")

num =180
listpagNum = []
for i in range(1,1000):
    print(i)
    num = num + 30
    try :#,200019,200041,200085,200091,200095,200096,200102,200105,200107,200109,200163wu,200210
       
        #爬取数据的地址
        urls ="写入自己的图像数据库地址"+str(num)
             
        print (urls);
        sleep(1)
        getUrl(urls)
    except SyntaxError:
        listpagNum.append(i)
        continu
    print(num)
print(listpagNum)







