import requests
import json
import pandas as pd
import time

import os
import db

apikey = os.getenv('APIKEY')

def getweather():
        r = requests.get('https://devapi.heweather.net/v7/weather/3d?location=101040700&key='+apikey)
        dic = json.loads(r.text).get('daily')
        today = dic[0]
        today['insertTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data= pd.DataFrame(today)
        db.insertWeather(data)

getweather()
