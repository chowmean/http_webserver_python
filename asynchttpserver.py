#author : chowmean
#http server
import socket
import threading
import SocketServer
import time
import json
import sys


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
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
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


