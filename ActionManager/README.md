
```
curl -v -XPOST http://127.0.0.1:5000/api/v1/entity -H "Content-Type:application/json" -d '{"name":"Test", "lat":33.333, "lon":35.33}'
```

```
curl -v -XPOST http://127.0.0.1:5000/api/v1/addaction -H "Content-Type:application/json" -d '{"id":"entity:1", "lat":33.333, "lon":35.33}'
```