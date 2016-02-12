import ctypes
import socket
import threading
import SocketServer
import time
import json
import sys


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



class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):


    def handle(self):
        data = self.request.recv(1024)
        data=data.split('&')
        request_data=dict()
        for dat in data:
        	t=dat.split('=')
        	request_data[t[0]]=t[1]
        print request_data
        print self
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


