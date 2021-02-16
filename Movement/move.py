import redis
import json
import time

r = redis.Redis()

while True:
    print("Waiting for tasks...");
    packed = r.blpop(['queue:movement'], 30)
    if not packed:
        continue
    data = json.loads(packed[1])
    print("Calculating movement for:{}".format(data['id']))


    #r.rpush('queue:movement',packed[1])


