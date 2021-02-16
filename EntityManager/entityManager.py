from flask import Flask,jsonify
import redis

#r = redis.Redis() #defauly localhost :6379
r = redis.StrictRedis('localhost',6379,decode_responses=True) #defauly localhost :6379

# How entity is stored in redis?
# Entity data is stored in HASHMAP,
# see redis commands for: HSET, HGETALL, HGET, HMSET
# Additionally, we have a SET to store entity ids
# and we have an auto incrementing counter eid to generate unique ids

def addEntity(name, latitude, longitude):
    id = r.incr('nextEntityId')  # get next id (returns number)

    eid = "entity:{}".format(id)  # generates entity id in format: "entity:id"
    r.hset(eid, mapping={"name": name,
                         "latitude": latitude, "longitude": longitude})

    # using one command
    #r.hset(eid, mapping={"latitude": latitude, "longitude": longitude})

    # or set each field independently
    #r.hset(eid, "latitude", 32.332)
    #r.hset(eid, "longitude", 32.332)

    # update SET of unique entity ids
    r.sadd("entities", eid)
    #e = r.hgetall(eid)
    #print(eid, e)


def getEntities():
    entity_ids = r.smembers("entities")
    entities = []
    for id in entity_ids:
        e = r.hgetall(id)
        entities.append(e)
    return entities

def initDBwithEntities():
    # delete old data, for debug
    r.delete('eid')
    entities = r.smembers("entities")
    for e in entities:
        r.delete(e)
    r.delete('entities')

    # add 5 entities
    for i in range(5):
        print("Adding new entity...")
        addEntity("CV90 #{}".format(i), 33.744, 34.003)

    # get the entities
    entities = getEntities()
    print("I've got {} entities".format(len(entities)))
    for e in entities:
        print(e)


#!flask/bin/python

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/entities',methods=['GET'])
def enitites():
    e = getEntities()
    return jsonify(e)

@app.route('/rachel')
def rachel():
    return "I'm Boaz"

if __name__ == '__main__':
    initDBwithEntities()
    app.run(debug=True)
    
