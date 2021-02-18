from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO
import os
import redis
import time
from config import Config

r = redis.StrictRedis('docksegenredis.redis.cache.windows.net',6380,password=Config.SECRET_KEY,decode_responses=True, ssl=True) #defauly localhost :6379

root = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "static", "dist")


app = Flask(__name__, static_url_path='', static_folder='static/dist')
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@socketio.on('get_entities')
def handle_message():
    print("getting entitites...")
    entity_ids = r.smembers("entities")
    print("Got {} entities...".format(len(entity_ids)))
    for eid in entity_ids:
        lat = r.hget(eid, 'lat')
        lon = r.hget(eid, 'lon')
        socketio.emit('entities.location', {"eid": eid, "lat": lat, "lon": lon})



def event_handler(msg):
    print('Handler:', msg)
    eid = msg["data"]
    lat = r.hget(eid, 'lat')
    lon = r.hget(eid, 'lon')
    print("lat,lon:{},{}".format(lat, lon))
    socketio.emit('entities.location', {
                  "eid": eid, "lat": lat, "lon": lon})


pubsub = r.pubsub()
pubsub.subscribe(**{'entities.location': event_handler})
thread = pubsub.run_in_thread(sleep_time=0.01)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    socketio.run(app,host='0.0.0.0',port=8080)
