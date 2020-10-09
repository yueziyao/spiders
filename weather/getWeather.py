import requests
import json

def getone():
        r = requests.get('https://devapi.heweather.net/v7/weather/3d?location=101040700&key=7e4459e12a764f1fa4bc134b2073d5bc')
        print(r)
        dic = json.loads(r)
        print(dic)

getone()