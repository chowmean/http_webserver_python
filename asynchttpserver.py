import ctypes
#author : chowmean
#http server
import socket
import threading
import SocketServer
import time
import json
import sys
import redis

redis_database = redis.StrictRedis(host='localhost', port=6379, db=0)

def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.isAlive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")




#=======================urlparserclass======================
def urlparser(resource):
	method=resource[0].split(' ')[0]
	url=resource[0].split(' ')[1]
	return method,url


#=============================request handler class==========


def create_request(data,thread):
	data_dict=dict()
	flag=0
	conntime=data.split('&')
	for a in conntime:
		data_dict[a.split('=')[0]]=a.split('=')[1]
	if 'connId' in data_dict:
		conn_id=data_dict['connId']
	else:
		flag=flag+1
	if 'timeout' in data_dict:
		timeout=data_dict['timeout']
	else:
		flag=flag+2
	redis_database.set(conn_id,thread.getName())
	redis_database.set(thread.getName,start_time)
	return 1

def get_thread_by_name(name):
	for a in threading.enumerate():
		if(a.getName()==name)
			return a
	return "error"


def get_thread_time(thread):
	name=thread.getName()
	start_time=redis_database.get(name)
	return time.time()-start_time



def give_server_status():
	re=dict()
	for key in redis_database.scan_iter():
		thread=get_thread_by_name(r.get(key))
		b=get_thread_time(thread)
		re['key']=b
	return re


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):


    def handle(self):
        start_time=time.time()
	data = self.request.recv(1024)
        data=data.split('&')
       
	request_data=dict()
	for dat in data:
        	t=dat.split('=')
        	request_data[t[0]]=t[1]
        method,url=urlparser(data)
	print method,url
	if(url.split('?')[0]=='api/request'):
		create_request(url.split('?')[1],threading.current_thread().getName(),start_time)
		work()
		a=dict()
	        a['status']="OK"
       		self.request.send("HTTP/1.1 200 OK\r\n" +
                               "Content-Type: application/json\r\n"+
                               "Connection: Alive\r\n")
        	self.request.send("\r\n")
        	self.request.send(json.dumps(a))


	elif(url=='serverStatus'):
		data=give_server_status()
		a=dict()
		a['severs']=data
                self.request.send("HTTP/1.1 200 OK\r\n" +
                               "Content-Type: application/json\r\n"+
                               "Connection: Alive\r\n")
                self.request.send("\r\n")
                self.request.send(json.dumps(a))



	for i in range(0,20):
		print i
		if threading.current_thread().getName()=='Thread-3':
                        break
		time.sleep(1)

        for a in threading.enumerate():
		print a.getName()
		if a.getName()=='Thread-2':
			thrd=a
			break
        for i in range (0,10):
		print i
		time.sleep(1)
		if i==5:
			try:
				terminate_thread(thrd)
				print "thread therminated succesfuly"
			except:
				print "error"
	#response = "{}: {}".format(cur_thread.name, data)
        a=dict()
        a['message']="success"
        self.request.send("HTTP/1.1 200 OK\r\n" +
                               "Content-Type: application/json\r\n"+
                               "Connection: Alive\r\n")
        self.request.send("\r\n")
        self.request.send(json.dumps(a))






class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass



if __name__ == "__main__":
    try:
		HOST=sys.argv[2]
    except:
		HOST='127.0.0.1'
    try:
		PORT=int(sys.argv[1])
    except:
		print "WARNING: Please specify port no. Exiting."
		exit()
	
    try:
   		val = int(PORT)
    except ValueError:
   		print("WARNING: Port number must be integer. Exiting.")
    
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    
    #t = threading.Thread(target=server.serve_forever,name='hero')
    #t.daemon=True
    #t.start()
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Listening on ", HOST,":",PORT
    server.serve_forever()
    #server.shutdown()
    #server.server_close()


