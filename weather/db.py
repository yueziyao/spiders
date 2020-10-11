import pymongo
import json
import os

username = os.getenv('DB_USERNAME')
url = os.getenv('DB_URL')
password = os.getenv('DB_PASSWORD')

def insertWeather(data):
    cleanData()
    cilent = pymongo.MongoClient(url,
        username=username,
        password=password,
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["daily"]
    str = json.loads(data.T.to_json()).values()

    res = collection.insert_many(str)
    

def cleanData():
    cilent = pymongo.MongoClient(url,
        username=username,
        password=password,
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["daily"]
    collection.remove()
    print('clean over')