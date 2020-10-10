import requests
import json
import pandas as pd
import time

import os
import db

def getweather():
        apikey = os.getenv('APIKEY')
        r = requests.get('https://devapi.heweather.net/v7/weather/3d?location=101040700&key='+apikey)
        dic = json.loads(r.text).get('daily')
        for d in dic:
                d['insertTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data= pd.DataFrame(dic)
        db.insertWeather(data)

getweather()
