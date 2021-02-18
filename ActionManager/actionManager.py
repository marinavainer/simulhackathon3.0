import redis
import json
from flask import Flask,jsonify,request,abort

#r = redis.Redis()
r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
        port=6379, 
        db=0, 
        password='', 
        ssl=False)

app = Flask(__name__)

@app.route('/api/v1/addaction', methods=['POST'])
def addActionRequest():
        print(request.json)
        if not request.json:
           abort(400)
        try:
            addAction(request.json["id"],request.json["lat"], request.json["lon"])
        except:
            abort(400)
        return jsonify({'status':'OK'})

# curl "http://127.0.0.1:5000/"  -d "name=bob" -d "lat=32.24545" -d "lon=35.656"

def addAction(entityId,lat,lon):
    data = {
            'id': entityId,
            'lat': lat,
            'lon' : lon
    }

    r.rpush('queue:movement',json.dumps(data))

    print("Adding new movement task")

if __name__ == '__main__':
    #addAction()
    print("hi")
    app.run(debug=True)