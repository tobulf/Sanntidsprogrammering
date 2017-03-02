from BaseHTTPServer import BaseHTTPRequestHandler
from UDP_driver  import UdpClient
from HTTP_driver import HttpServer
from json import loads, dumps
from threading import Thread
from Client import Client
from TypeClasses import*
from QueueMaster import QueueMaster
from time import sleep



# Testing shit
Bcast = "129.241.187.255"
IP    = "129.241.187.159"
Port  = 20010

data  = dumps(["all good"])

queuemaster = QueueMaster()


# RequestHandler Wich Does all the work for the server:
class RequestHandler(BaseHTTPRequestHandler):
    # custom made handler class for the networkmodule:
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0)) #Finding the length of the response body
        body = self.rfile.read(content_len) #Extracting the body
        try:
            Clientobject = Client()
            # Load Clientobject from json
            Clientobject.fromJson(body)
            # Answer is calculated and serialized directly
            if self.path == "Got Order":
                answer = queuemaster.GotOrder(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            elif self.path == "Get Update":
                answer = queuemaster.GetUpdate(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            else:
                answer = ""
                self.send_response(200, answer) #Send the proper response and status
        except TypeError:
            pass

    def do_GET(self):
        # Only dormant server post Get
        answer = queuemaster.toJson()
        self.send_response(200, answer)





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
    #Thread_1.start()
    print "running"
    #Thread_1.join()
    Thread_2.join()
main()






