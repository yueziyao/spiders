import pymongo
import json

def insertWeather(data):
    cilent = pymongo.MongoClient('mongodb://yzy.myqnapcloud.cn:32774/',
        username="iced",
        password='iced',
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["daily"]
    str = json.loads(data.T.to_json()).values()

    res = collection.insert_many(str)
    cleanData()

def cleanData():
    cilent = pymongo.MongoClient('mongodb://yzy.myqnapcloud.cn:32774/',
        username="iced",
        password='iced',
        authSource='admin',
        authMechanism='SCRAM-SHA-1')

    db = cilent["app"] #连接mydb数据库，没有则自动创建
    collection = db["daily"]
    for id in collection.distinct('fxDate'):#使用distinct方法，获取每一个独特的元素列表
        num = collection.count({"fxDate":id})#统计每一个元素的数量
        if(num > 1):
            a = collection.find({"fxDate":id}).sort('time',pymongo.ASCENDING)
            lists = list(a)
            collection.remove({"fxDate":id ,'insertTime':lists[0]['insertTime']},0)
            print('重复issue数据 id = %s ,删除入库时间： %s,保留入库时间：%s' %(id,lists[0]['insertTime'],lists[1]['insertTime']))
