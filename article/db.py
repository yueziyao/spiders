import pymongo
import json
import os

username = os.getenv('DB_USERNAME')
url = os.getenv('DB_URL')
password = os.getenv('DB_PASSWORD')

def insertData(data):
    cilent = pymongo.MongoClient(url,
        username=username,
        password=password,
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["articles"]
    str = json.loads(data.T.to_json()).values()

    res = collection.insert_many(str)
    cleanData()

def cleanData():
    cilent = pymongo.MongoClient(url,
        username=username,
        password=password,
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["articles"]
    for id in collection.distinct('name'):#使用distinct方法，获取每一个独特的元素列表
        num = collection.count({"name":id})#统计每一个元素的数量
        if(num > 1):
            a = collection.find({"name":id}).sort('time',pymongo.ASCENDING)
            lists = list(a)
            collection.remove({"name":id ,'time':lists[0]['time']},0)
            print('重复issue数据 id = %s ,删除入库时间： %s,保留入库时间：%s' %(id,lists[0]['time'],lists[1]['time']))
