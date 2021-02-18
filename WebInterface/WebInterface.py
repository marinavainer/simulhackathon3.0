from flask import Flask, request, render_template, flash, redirect, jsonify, json
import redis

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

#r = redis.Redis() #defauly localhost :6379
#r = redis.StrictRedis('localhost',6379,decode_responses=True) #defauly localhost :6379
r = redis.StrictRedis(host='docksegenredis.redis.cache.windows.net',
       port=6379, db=0, password='6zfJhTMLb9Vi9aF9ND6f5tBybpgQdlXv2Aaf6LjkUV8=', ssl=False)

# How entity is stored in redis?
# Entity data is stored in HASHMAP,
# see redis commands for: HSET, HGETALL, 0, HMSET
# Additionally, we have a SET to store entity ids
# and we have an auto incrementing counter eid to generate unique ids


def addEntity(name, latitude, longitude):
    id = r.incr('nextEntityId')  # get next id (returns number)

    eid = "entity:{}".format(id)  # generates entity id in format: "entity:id"
    r.hset(eid, mapping={"name": name,
                         "lat": latitude,
                         "lon": longitude})

    # update SET of unique entity ids
    r.sadd("entities", eid)
    return eid


def getEntityById(eid):
    entityDetails = r.hgetall(eid)
    return entityDetails
    

def getEntities():
    entity_ids = r.smembers("entities")
    entities = []
    entitiesbinary =[]
    pipe = r.pipeline()
    for id in entity_ids:
        eid = id.decode("utf-8")
        pipe.hgetall(eid)
        entity = {}
        entity['id'] = id.decode("utf-8")
        entities.append(entity)
  
    entitiesbinary = pipe.execute()

    i = 0
    for entitybinary in entitiesbinary:
        entity = entities[i]
        i = i + 1
        entity['name'] = entitybinary[bytes(b'name')].decode("utf-8")
        entity['lat'] = entitybinary[bytes(b'lat')].decode("utf-8")
        entity['lon'] = entitybinary[bytes(b'lon')].decode("utf-8")

    return entities

    
def getEntity():

    id = 'entity:' + str(1)
    e = r.hgetall(id)
    for field in e:
        field = field.decode("utf-8")
    return e

def CleanDatabase():
    entities = r.smembers("entities")
    for e in entities:
        r.delete(e)
    r.delete('entities')   

def GetEntityNumber():
    # get the entities
    entities = getEntities()
    return len(entities)

class NewEntityForm(FlaskForm):
    entityName = StringField('entityName', validators=[DataRequired()])
    latitude = StringField('latitude', validators=[DataRequired()])
    longitude = StringField('longitude', validators=[DataRequired()])
    submit = SubmitField('Create Entity')


@app.route('/')
def index():
    return redirect('/entities')


@app.route('/entityDetails')
def entityDetails():
    e = getEntity()
    return jsonify(e)


@app.route('/dropDB')
def dropDB():
    CleanDatabase()
    return redirect('/entities')


@app.route('/entities', methods=['GET', 'POST'])
def entities():
    if request.method == "POST":
        req = request.form
        entityDetails = {}
        entityDetails['eid'] = req.get('eid')
        entityDetails['lat'] = req.get('lat')
        entityDetails['lon'] = req.get('lon')
        entityDetails['vel'] = req.get('vel')
        #return redirect('/MoveEntity')
        return render_template('MoveEntity.html', title='Move entity', entityDetails=entityDetails)
    else:
        entities = getEntities()
        return render_template('Entities.html', title='Entities list', entities=entities)


@app.route('/create_entity', methods=['GET', 'POST'])
def createEntity():
    if request.method == "POST":
        req = request.form
        name = req["entityName"]
        lat = req["latitude"]
        lon = req["longitude"]
        addEntity(name, lat, lon)    
        return redirect('/entities')
    form = NewEntityForm()
    return render_template('CreateEntity.html', title='Create entity', form=form)


@app.route('/displayMap')
def displayMap(): 
    entities = getEntities()
    return render_template('map.html', title='entities on map', entities=json.dumps(entities))


@app.route('/GetUpdatedPositions', methods=['POST'])
def GetUpdatedPositions():
    entities = getEntities()
    return json.dumps(entities)

if __name__ == '__main__':
    app.run(debug=True)
    
