from BaseHTTPServer import BaseHTTPRequestHandler
from json import dumps
from threading import Thread,Lock
from HTTPServer import HttpServer
from HTTPClient import HttpClient
from Client import Client
from QueueMaster import QueueMaster
from UDPClient  import UdpClient
from TypeClasses import*

# Testing shit
Bcast = "129.241.187.255"
IP    = "129.241.187.150"
Port  = 20010


# Declare the queuemasterobject for this server
queuemaster = QueueMaster()

# RequestHandler which Does all the work for the server:
class RequestHandler(BaseHTTPRequestHandler):
    # Custom made handler class for the Networkmodule:
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0)) #Finding the length of the response body
        body = self.rfile.read(content_len) #Extracting the body
        try:
            # Declare the Client object to receive:
            Clientobject = Client()
            # Answer is calculated and serialized directly
            if self.path == "Got Order":
                # Load Clientobject from json
                Clientobject.fromJson(body)
                answer = queuemaster.GotOrder(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            elif self.path == "Get Update":
                # Load Clientobject from json
                Clientobject.fromJson(body)
                answer = queuemaster.GetUpdate(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            else:
                answer = "Path Dont exist"
                self.send_response(404, dumps(answer)) #Send the proper response and status
        except TypeError:
            pass

    def do_GET(self):
        # Only dormant server post Get:
        answer = queuemaster.toJson()
        self.send_response(200, answer)

Handler = RequestHandler
server  = HttpServer(IP, Port, Handler)
server.serving = True
heartbeat = UdpClient(Bcast, IP, Port)
state = ServerState.Listening
# Declares a Client, binds it to port zero and local.
backupclient  = HttpClient("",0)
# Mutex
Mutex = Lock()

def Threadfunction1():
    while True:
        if heartbeat.ServingServer:
            # Serve request:
            server.ServeOnce()
            # Check for Timeouts
            queuemaster.CheckTimeout()
        else:
            queuemaster = backupclient.GetRequest()



def Threadfunction2():
    while True:
        if heartbeat.ServingServer:
            heartbeat.Heartbeat()
        else:
            Mutex.acquire()
            heartbeat.ServerListen()
            Mutex.release()
            if heartbeat.ServingServer:
                pass
            else:
                # Bind the Client to the Ip and port of current serving server:
                Mutex.acquire()
                backupclient = HttpClient(heartbeat.ServerAdress[0], heartbeat.ServerAdress[1])
                Mutex.release()







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






