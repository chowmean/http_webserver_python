#Simple HTTP webserver
##This is made using SOCKETSERVER

###How to use:
- Install redis server

``` sudo apt-get install redis-server```

- Run redis server

``` redis-server ```

- Run the file with HOST and PORT input from command line 

``` python asynchttpserver.py 8080 0.0.0.0 ```

###Endpoints

- Get /api/request?connId=12&timeout=120
- Get /serverStatus
- Post /api/kill   `{'connId':Int}`


###Features
- [x] Multithreading
- [x] Handling all type of requests.
- [ ] Error Handling
- [x] Adding function to kill the request in between.
- [x] URL handling and mapping
- [x] Implementing cache using redis




###Debuging options

- Try cleaning your redis server everytime you restart the server. If any stray data is present it will cause deviations.

- Run these commands to do so in python shell

``` import python
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for key in r.scan_iter():
                print key, r.delete(key)
```


__author__ :  chowmean
