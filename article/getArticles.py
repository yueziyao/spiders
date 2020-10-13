# -*- coding: utf-8 -*-
import pandas as pd
import requests
import time
import json
from db import *

def getJuejinHotWeekly():
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://e.xitu.io',
        'Referer': 'https://e.xitu.io/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    api_url = "https://extension-ms.juejin.im/resources/gold"
    reqdata = {'category': 'frontend', 'order': 'heat', 'offset': 0, 'limit': 15}
    res = requests.post(
        api_url,
         json.dumps(reqdata).encode("utf-8"),
        headers=headers
    )
    res = res.content.decode('utf-8')
    code = json.loads(res).get('code')
    datas =[]
    if code == 200:
         datas = json.loads(res)

    x = datas['data']
    lists = []
    for li in x:
        data = {
            "name": li["title"],
            "url": li["url"],
            "date": li["date"]["iso"],
            "time": time.time(),
            "from": "juejin",
        }
        lists.append(data)
    print(lists)
    return lists

def getUisdcHot():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Connection': 'close'}
    api_url = "https://www.uisdc.com/ajax.php"
    reqdata = "action=hot_posts&ppp=16"
    res = requests.post(
        api_url,
        reqdata,
        headers=headers
    )
    res = res.content.decode('utf-8')
    lists = json.loads(res).get('data')
    x = []
    for item in lists:
        article = {
            "name": item["title"],
            "url": item["href"],
            "author": item["author"],
            "date": item["time"],
            "img": item["img"],
            "zan": item["zan"],
            "from": "uisdc",
            "time": time.time(),
        }
        x.append(article)
    # 解析
    return x

def get75Hot():
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
    api_url = "https://www.zhihu.com/api/v4/columns/75weekly/items"
    res = requests.get(url=api_url,headers=Headers)
    res = res.content.decode('utf-8')
    lists = json.loads(res).get('data')
    x = []
    for item in lists:
        c = time.localtime(item["created"])
        article = {
            "name": item["title"],
            "url": item["url"],
            "author": item["author"]['name'],
            "content": item['content'],
            "date": time.strftime("%Y-%m-%d",c),
            "img": item["image_url"],
            "zan": item["voteup_count"],
            "from": "75",
            "time": time.time(),
        }
        x.append(article)
    # 解析
    return x

# 数据处理、入库
# get75Hot()
# getJuejinHotWeekly()
# getUisdcHot()
data1 = pd.DataFrame(getUisdcHot())
insertData(data1)
data2 = pd.DataFrame(getJuejinHotWeekly())
insertData(data2)
data3 = pd.DataFrame(get75Hot())
insertData(data3)

print("数据录入成功")
