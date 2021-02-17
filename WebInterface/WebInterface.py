from flask import Flask, request, render_template, flash, redirect, jsonify, json
import redis

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

#r = redis.Redis() #defauly localhost :6379
r = redis.StrictRedis('localhost',6379,decode_responses=True) #defauly localhost :6379

# How entity is stored in redis?
# Entity data is stored in HASHMAP,
# see redis commands for: HSET, HGETALL, 0, HMSET
# Additionally, we have a SET to store entity ids
# and we have an auto incrementing counter eid to generate unique ids


def addEntity(name, latitude, longitude):
    id = r.incr('nextEntityId')  # get next id (returns number)

    eid = "entity:{}".format(id)  # generates entity id in format: "entity:id"
    r.hset(eid, mapping={"name": name,
                         "latitude": latitude,
                         "longitude": longitude})

    # update SET of unique entity ids
    r.sadd("entities", eid)
    return eid


def getEntityById(eid):
    entityDetails = r.hgetall(eid)
    return entityDetails


def getEntities():
    entity_ids = r.smembers("entities")
    entities = []
    for id in entity_ids:
        e = r.hgetall(id)
        e['id'] = id
        entities.append(e)

    return entities
    

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
    #return jsonify(entities)
    return render_template('map.html', title='entities on map', entities=json.dumps(entities))


if __name__ == '__main__':
    app.run(debug=True)
    
