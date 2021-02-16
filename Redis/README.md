# python virtual environment
```bash
pyhton -mvenv hack
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
docker run --network hackaton --rm --name redis-cli -it redis redis-cli -h hackathon-redis
```
stop
```bash
docker stop hackaton-redis

```
# Web Api
pip install flask redis


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
