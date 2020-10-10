# -*- coding: utf-8 -*-
import pandas as pd
import requests
from db import *
import time
import json

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


# 数据处理、入库
data = pd.DataFrame(getJuejinHotWeekly())
re = insertData(data)
print("数据录入成功")
