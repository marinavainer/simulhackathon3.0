import redis
import json

r = redis.Redis()
for i in range(5):
    data = {
            'id': i+1,
            'name': 'tank #{}'.format(i+1)
    }
    r.rpush('queue:movement',json.dumps(data))
    print("Adding new movement task")


