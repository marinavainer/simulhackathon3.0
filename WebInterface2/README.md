# Introduction
This uses OpenLayers map,
See their site: https://openlayers.org/en/latest/examples/

In order to get real-time data, it uses websocket (socketio) to get data in real time from backend server.

Backed server uses redid pub/sub to be notified about location updates, and forwards this updates via websocket to the web site.


See move.py in Movement,
You should publish this, after location change.
```python
# send notification on location change
r.publish("entities.location", eid)
```

# THIS ONLY SHOWS LOCATION UPDATES
# IF YOU NEED TO SHOW INITALLY ALL ENTITIES - ADD RELEVANT CODE TO FETCH ALL ENTITIES AND SHOW THEIR LOCATION
## See static/main.js
```js
//1. get all entities from your service
//2. source.clear() //remove all markers
//3. for each entity:
var icon = new Feature({
      type: 'icon',
      geometry: new Point(fromLonLat([k.lon, k.lat])),
    });
source.addFeature(icon);
```

# Build instructions

In order to build it, your need nodejs,    
but in CONTAINER, you do not need to have node installed

```bash
cd static
npm install
npm run build
#this creates dist folder  (compiled web site)
cd ..
pip install flask-socketio
```

# Running
```bash
python app.py
```

# Docker:
In docker you need to have:

/app/app.py
/app/static/dist

# Good luck



