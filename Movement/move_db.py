import redis
import json
import time

#r = redis.Redis()

r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
        port=6379, db=0, password='6zfJhTMLb9Vi9aF9ND6f5tBybpgQdlXv2Aaf6LjkUV8=', ssl=False)

while True:
    #entities = getEntities()
    #id = 'entity:1' # input("enter entity id: ")
    #entity = getEntity(id)

    tic = time.perf_counter()
    for i in range(100):
        id = 'entity:' + str(i)
        
        # get location as floats
        lat = float(r.hget(id, 'lat'))
        lon = float(r.hget(id, 'lon'))
        #print(lat, lon)
    
        # move the entity
        lat +=  0.0001
        lon +=  0.0001

        # update db 
        r.hset(id,'lat', lat)
        r.hset(id, 'lon', lon)

    toc = time.perf_counter()
    print(f"TimeGet: {toc - tic:0.4f} seconds")
    # get location as floats
    #lat = float(r.hget(id, 'lat'))
   # lon = float(r.hget(id, 'lon'))
   # print(lat, lon)

    print("cycle end")
    time.sleep(2)    # Pause 5.5 seconds


