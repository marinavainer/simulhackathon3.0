# python virtual environment
```bash
python -m venv hack
hack/Scripts/activate.bat
```

```bash
#deactivate virtual environment
deactivate
```


# redis Docker
```bash
docker ps
```
pull & start redis docker in background
```bash
docker run --network hackathon --name hackathon-redis -p6379:6379 -d redis
```
start redis-cli
```bash
docker run --network hackathon --rm --name redis-cli -it redis redis-cli -h hackathon-redis
```
stop
```bash
docker stop hackaton-redis

```

# redis Docker Azure
Create "Azure Cache for Redis"
Go to Propeties and copy YOURHOSTNAME
Go to Access keys and copy PRIMARY_ACCESS_KEY

start redis-cli
```bash
docker run --rm -it redis redis-cli -h YOURHOSTNAME -a PRIMARY_ACCESS_KEY
```

from redis-cli
```
hgetall entity:1
llen queue:movement
```

# Web Api
```bash
pip install flask redis
```
A minimalistic web api project
```python
from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
```
