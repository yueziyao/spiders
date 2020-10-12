# -*- coding: utf-8 -*-
#import pandas as pd
import requests
import time
import json
from article.db import insertData


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
    # headers = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    # response = requests.get( url='https://www.uisdc.com/', headers=headers)
    # soup = BeautifulSoup(response.text, "html.parser")
    # list = soup.select('.articles-hot')
    # print(list);
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
        }
        x.append(article)
    # 解析
    return x

# 数据处理、入库
# getJuejinHotWeekly()
# getUisdcHot()
data1 = pd.DataFrame(getUisdcHot())
insertData(data1)
data2 = pd.DataFrame(getJuejinHotWeekly())
insertData(data2)

print("数据录入成功")
