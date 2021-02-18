import redis
import json
import time
import threading
import pyproj

from pyproj import Proj

#sr = redis.Redis()

r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
                      port=6379, db=0, password='', ssl=False)


def movementThread(eid, sLat, sLon, eLat, eLon):
    print("Movement task thread for {} - started.".format(eid))

    myProj = Proj(
        "+proj=utm +zone=36U, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    xStart, yStart = myProj(sLon, sLat)
    xEnd, yEnd = myProj(eLon, eLat)

    deltaX = xEnd - xStart
    deltaY = yEnd - yStart
    print(deltaX, deltaY)

    steps = 1000
    xStep = deltaX / steps
    yStep = deltaY / steps

    xCurr = xStart
    yCurr = yStart

    for step in range(steps):
        # move step
        xCurr += xStep
        yCurr += yStep

        # convert back to geo coordinate
        lon, lat = myProj(xCurr, yCurr, inverse=True)

        # update db
        r.hset(eid, 'lat', lat)
        r.hset(eid, 'lon', lon)
        # send notification on location change
        r.publish("entities.location", eid)
    print("Movement task thread for {} - finished.".format(eid))


while True:
    print("Waiting for movement tasks...")
    packed = r.blpop(['queue:movement'], 30)
    if not packed:
        continue

    print("Got new task.")
    tic = time.perf_counter()

    # get entity id & end point location
    data = json.loads(packed[1])
    id = data[0]['id']
    eLat = data[0]['lat']
    eLon = data[0]['lon']
    eid = 'entity:' + str(id)

    # get location as floats
    sLat = float(r.hget(eid, 'lat'))
    sLon = float(r.hget(eid, 'lon'))

    # move the entity
    x = threading.Thread(target=movementThread,
                         args=(eid, sLat, sLon, eLat, eLon,))
    x.start()

    toc = time.perf_counter()
    print(f"Ready for another task. time elapsed: {toc - tic:0.4f} seconds")
