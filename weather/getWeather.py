import requests
import json
import pandas as pd
import time

import db

def getweather():
        r = requests.get('https://devapi.heweather.net/v7/weather/3d?location=101040700&key=7e4459e12a764f1fa4bc134b2073d5bc')
        dic = json.loads(r.text).get('daily')
        for d in dic:
                d['insertTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data= pd.DataFrame(dic)
        db.insertWeather(data)

getweather()
