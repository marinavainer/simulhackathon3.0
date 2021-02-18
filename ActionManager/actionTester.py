import redis
import json

#r = redis.Redis()

#'lat': 32.212750895854434
#'lon': 34.978807518673285

r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
        port=6379, db=0, password='=', ssl=False)

for i in range(100):
        
        # init entities in different start point locations
        delta = 0.001 * i
        lat = 32.226402272851416 + delta
        lon = 34.9905663231064 + delta

        eid = 'entity:' + str(i)
        name = 'marina' + str(i)
        r.hset(eid, mapping={"name": name, "lat": lat, "lon": lon})

        #r.hset(eid, 'lat', lat)
        #r.hset(eid, 'lon', lon)
        
        r.sadd("entities", eid)

         # request entities in the same end point locations
        data = {
                'id': i,
                'lat': 32.15317153318547,
                'lon': 34.85844350806958
        },

        r.rpush('queue:movement',json.dumps(data))
        print("movement task added")

