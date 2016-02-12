#Simple HTTP webserver
##This is made using SOCKETSERVER

###How to use:
- Install redis server
``` sudo apt-get install redis-server```
- Run redis server
```redis-server```
- Run the file with HOST and PORT input from command line 
```python asynchttpserver.py 8080 0.0.0.0```

###Endpoints

- Get /api/request?connId=12&timeout=120

###Features
- [x] Multithreading
- [x] Handling all type of requests.
- [ ] Error Handling
- [ ] Adding function to kill the request in between.
- [ ] URL handling and mapping
- [ ] Implementing cache using redis

__author__ :  chowmean
