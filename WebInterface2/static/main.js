
import 'ol/ol.css';
import Feature from 'ol/Feature';
import { default as OlMap } from 'ol/Map';
import Point from 'ol/geom/Point';
import Polyline from 'ol/format/Polyline';
import VectorSource from 'ol/source/Vector';
import View from 'ol/View';
import OSM from 'ol/source/OSM';
import { fromLonLat } from 'ol/proj';
import {
  Circle as CircleStyle,
  Fill,
  Icon,
  Stroke,
  Style,
} from 'ol/style';

import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import { getVectorContext } from 'ol/render';
import socketIOClient from 'socket.io-client';
const endpoint = "http://127.0.0.1:4001";
const io = socketIOClient();


var entities = new Map();



var center = [-5639523.95, -3501274.52];
var map = new OlMap({
  target: document.getElementById('map'),
  view: new View({
    center: center,
    zoom: 10,
    minZoom: 2,
    maxZoom: 19,
  }),
  layers: [
    new TileLayer({
      source: new OSM(),
    })],
});

var styles = {
  'route': new Style({
    stroke: new Stroke({
      width: 6,
      color: [237, 212, 0, 0.8],
    }),
  }),
  'icon': new Style({
    image: new Icon({
      anchor: [0.5, 1],
      src: 'marker.png',
    }),
  }),
  'geoMarker': new Style({
    image: new CircleStyle({
      radius: 7,
      fill: new Fill({ color: 'black' }),
      stroke: new Stroke({
        color: 'white',
        width: 2,
      }),
    }),
  }),
};

var source = new VectorSource({
  features: [],
});
var vectorLayer = new VectorLayer({
  source: source,
  style: function (feature) {
    return styles[feature.get('type')];
  },
});

map.addLayer(vectorLayer);


io.on('entities.location', (msg) => {
  console.log('socketio:', msg);
  entities.set(msg.eid, msg);
  console.log(entities);
  source.clear();
  entities.forEach((k) => {
    console.log('adding icon for location:', k);
    //let e = entities.get(k);
    var icon = new Feature({
      type: 'icon',
      geometry: new Point(fromLonLat([k.lon, k.lat])),
    });
    source.addFeature(icon);
  });
});

// The polyline string is read from a JSON similiar to those returned
// by directions APIs such as Openrouteservice and Mapbox.
/*fetch('data/polyline/route.json').then(function (response) {
  response.json().then(function (result) {
    var polyline = result.routes[0].geometry;

    var route = new Polyline({
      factor: 1e6,
    }).readGeometry(polyline, {
      dataProjection: 'EPSG:4326',
      featureProjection: 'EPSG:3857',
    });

    var routeFeature = new Feature({
      type: 'route',
      geometry: route,
    });
    var geoMarker = new Feature({
      type: 'geoMarker',
      geometry: new Point(route.getCoordinateAt(0)),
    });
    var startMarker = new Feature({
      type: 'icon',
      geometry: new Point(route.getCoordinateAt(0)),
    });
    var endMarker = new Feature({
      type: 'icon',
      geometry: new Point(route.getCoordinateAt(1)),
    });



    var animating = false;

    var vectorLayer = new VectorLayer({
      source: new VectorSource({
        features: [routeFeature, geoMarker, startMarker, endMarker],
      }),
      style: function (feature) {
        // hide geoMarker if animation is active
        if (animating && feature.get('type') === 'geoMarker') {
          return null;
        }
        return styles[feature.get('type')];
      },
    });

    map.addLayer(vectorLayer);

    var speed, startTime;
    var speedInput = document.getElementById('speed');
    var startButton = document.getElementById('start-animation');

    function moveFeature(event) {
      var vectorContext = getVectorContext(event);
      var frameState = event.frameState;

      if (animating) {
        var elapsedTime = frameState.time - startTime;
        var distance = (speed * elapsedTime) / 1e6;

        if (distance >= 1) {
          stopAnimation(true);
          return;
        }

        var currentPoint = new Point(route.getCoordinateAt(distance));
        var feature = new Feature(currentPoint);
        vectorContext.drawFeature(feature, styles.geoMarker);
      }
      // tell OpenLayers to continue the postrender animation
      map.render();
    }

    function startAnimation() {
      if (animating) {
        stopAnimation(false);
      } else {
        animating = true;
        startTime = new Date().getTime();
        speed = speedInput.value;
        startButton.textContent = 'Cancel Animation';
        // hide geoMarker
        geoMarker.changed();
        // just in case you pan somewhere else
        map.getView().setCenter(center);
        vectorLayer.on('postrender', moveFeature);
        map.render();
      }
    }

    function stopAnimation(ended) {
      animating = false;
      startButton.textContent = 'Start Animation';

      // if animation cancelled set the marker at the beginning
      var coord = route.getCoordinateAt(ended ? 1 : 0);
      geoMarker.getGeometry().setCoordinates(coord);
      // remove listener
      vectorLayer.un('postrender', moveFeature);
    }

    startButton.addEventListener('click', startAnimation, false);
  });
});*/
