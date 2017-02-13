from BaseHTTPServer import BaseHTTPRequestHandler
from UDP_driver  import UdpClient
from HTTP_driver import HttpServer
from json import loads,dumps
from threading import Thread
from Queue import Queue
from time import sleep

# Declaring a list for current clients:
ClientList = []
# Testing shit
Bcast = "129.241.187.255"
IP    = "129.241.187.143"
Port  = 20010

data  = dumps(["all good"])



class RequestHandler(BaseHTTPRequestHandler):
    # custom made handler class for the networkmodule:
    def do_POST(self):
        # Adds the client to the Clientlist:
        if not self.client_address in ClientList:
            #if the served client is not in the client list, it is added
            ClientList.append(self.client_address)
        path = self.path
        content_len = int(self.headers.getheader('content-length', 0)) #Finding the length of the response body
        body = self.rfile.read(content_len) #Extracting the body
        try:
            received = loads(body)
            print received[0]
            #handle the request trough the queue module:
            #data = dumps(UpdateQueue(received))
            self.send_response(200, data) #Send the proper response and status
        except TypeError:
            pass
handler = RequestHandler
server = HttpServer(IP, Port, handler)
server.serving = True
heartbeat = UdpClient(Bcast, IP, Port )


def Threadfunction1():
    while True:
        server.Serve()

def Threadfunction2():
    while True:
        heartbeat.ServerListen()




# several request Works fine, handler and server coping good, need only 2 threads!:

def main():
    Thread_1 = Thread(target= Threadfunction1, args = (),)
    Thread_2 = Thread(target= Threadfunction2, args = (),)
    Thread_2.start()
    Thread_1.start()
    print "running"
    Thread_1.join()
    Thread_2.join()
main()






