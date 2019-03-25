# coding=utf-8
'''
   功能：爬取视频图像（谷歌浏览器）
   1、修改Host和从cookie
   2、
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
               'Cookie': 'JSESSIONID=49840976216FB769E70E63070C15D24C',
               'Host': '121.201.83.194:8040',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
               }

    # cookies = {
    # }
    #请求设置页眉
    resultPage = requests.get(urls, headers=headers)
    soup = BeautifulSoup(resultPage.text)
    scrr = soup.find('p')
    print(scrr)

    lst = scrr.text
    j = json.loads(lst)
    print(type(j))
    print(type(j['rows']))
    rowslst = j['rows']


    # mp4lst = []
    # for rl in rowslst:
    #     print(type(rl))
    #     print(rl['imgUrls'])
    #     urls = rl['imgUrls']
    #
    #     for ls in urls:
    #         if str(ls).endswith('.mp4'):
    #             mp4lst.append(ls)
    #
    # mps = set(mp4lst)
    # print(mp4lst)
    # print(mps)
    # i = 1
    # for url in mps:
    #     strss = str(url).split("/")
    #     name = strss[-1]
    #
    #     dest_resp = requests.get(url)
    #     # 视频是二进制数据流，content就是为了获取二进制数据的方法
    #     data = dest_resp.content
    #     path = u'C:/Users/Desktop/mp4/' + str(name)
    #     f = open(path, 'wb')
    #     f.write(data)
    #     f.close()
    #     i = i + 1

    #代码爬去通道为1的图片数据
    imgLst = []
    for tab in lst:
        print(tab)
        if not str(tab).startswith("{"):

            tab = "{"+tab
        d1 = eval(tab)
        if d1["cameraNo"] == 1:
           # print(d1["imgUrl"])
            imgLst.append(d1["imgUrl"])
    print (imgLst)
    for img in imgLst:
        print(img)
        try:
            urllib.request.urlretrieve(img, 'E:/code with lief/%s.jpg' % int(round(time.time() * 1000)))
        except urllib.error.HTTPError:
            continue
    print("over")

for i in range(0,1):
    try :
        urls = "（写入网站地址）&startTime=2019-02-25%2000:00:00&endTime=2019-02-25%2011:06:19&dbKey=dbGzky"
        print (urls);
        sleep(1)
        getUrl(urls)

    except SyntaxError:
        continue
      








