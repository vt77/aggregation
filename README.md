Domains statistics system
---

# Overview 
This project is a domain statistcs system wrote for test
It's a flask+swagger API application

# Install dependency

```
pip install -r requirements.txt
```

## Dependency
1. gevent
2. cachetools 

# Running test 
1. Run flask application 
```
FLASK_APP=app.py flask run
```
or  use ./start.sh

2. Post some test data

```
./send_domains_stats.sh
```
You can run send stats script multiply times 

3. Wait for next statistics period 

4. Use stats endpoint to get stats
```
curl -X GET "http://127.0.0.1:5000/domains/min" -H "accept: application/json"
```

# Debugging and monitoring

Program writes log to stdout 

Example : 
```
INFO:werkzeug:127.0.0.1 - - [09/Feb/2022 13:48:54] "POST /domains HTTP/1.1" 200 -
DEBUG:root:[API]Process append request  {'timestamp': 1644407344, 'example1.com': 80, 'example2.com': 5, 'example3': 12}
DEBUG:root:[API]Add domain stats : example1.com => 80
DEBUG:storage.memory:[STORAGE][1644407344]Save clicks for 1 -  80 
DEBUG:storage.memory:[STORAGE][CLICK]Request cache size : 1
DEBUG:root:[API]Add domain stats : example2.com => 5
DEBUG:storage.memory:[STORAGE][1644407344]Save clicks for 2 -  5 
DEBUG:storage.memory:[STORAGE][CLICK]Request cache size : 1
DEBUG:root:[API]Add domain stats : example3 => 12
DEBUG:storage.memory:[STORAGE][1644407344]Save clicks for 3 -  12 
DEBUG:storage.memory:[STORAGE][CLICK]Request cache size : 1
INFO:werkzeug:127.0.0.1 - - [09/Feb/2022 13:48:54] "POST /domains HTTP/1.1" 200 -
DEBUG:root:[APP]Rebuild aggregation min
DEBUG:storage.memory:[STORAGE] Get clicks for domain example1.com
DEBUG:storage.memory:[STORAGE] Get clicks for domain example2.com
DEBUG:storage.memory:[STORAGE] Get clicks for domain example3
DEBUG:root:[APP][min]Top domains {'domains': {'example3': 144, 'example1.com': 110, 'example2.com': 95}}
INFO:root:[API]Getting top domains list for min
INFO:werkzeug:127.0.0.1 - - [09/Feb/2022 13:49:16] "GET /domains/min HTTP/1.1" 200 -
```
