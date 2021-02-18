from flask import Flask,jsonify
import redis

#r = redis.Redis() #defauly localhost :6379
r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
        port=6379, 
        db=0, 
        password='', 
        ssl=False)

def getEntities():
    entity_ids = r.smembers("entities")
    entities = []
    for id in entity_ids:
        e = r.hgetall(id)
        entities.append(e)
    return entities


def getEntitiesPipeline():
    entity_ids = r.smembers("entities")
    entities = []
    pipe = r.pipeline()
    for id in entity_ids:
        pipe.hgetall(id)

    entities = pipe.execute()
    return entities

if __name__ == '__main__':
    entities = getEntitiesPipeline()  
    #entities = getEntities() 
    print(entities)
