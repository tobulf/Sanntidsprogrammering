from BaseHTTPServer import BaseHTTPRequestHandler
from json import dumps
from threading import Thread,Lock

from Client import Client
from HTTPServer import HttpServer
from QueueMaster import QueueMaster

from HTTPClient import HttpClient
from TypeClasses import*
from UDPClient  import UdpClient

# Testing shit
Bcast = "129.241.187.255"
IP    = "129.241.187.143"
Port  = 20010

from UDPClient  import UdpClient
import netifaces as FindIP
from Timer import Timer


# Finding the IP:
FindIP.ifaddresses('eth0')
IP = FindIP.ifaddresses('eth0')[2][0]['addr']
Bcast = FindIP.ifaddresses('eth0')[2][0]['broadcast']
Port  = 20011



# Declare the queuemasterobject for this server
Queuemaster = QueueMaster()
# Heartbeat object:
heartbeat = UdpClient(Bcast, IP, Port)
# Declares a Client, binds it to port zero and local.
backupclient = HttpClient("",0)
# Mutex
Mutex = Lock()
# Request-Timer T keep the Dormant server from Spamming to much requests:
RequestTimer = Timer()


# RequestHandler which Does all the work for the server:
class RequestHandler(BaseHTTPRequestHandler):
    # Custom made handler class for the Networkmodule:
    def do_POST(self):
        global Queuemaster
        content_len = int(self.headers.getheader('content-length', 0)) #Finding the length of the response body
        body = self.rfile.read(content_len) #Extracting the body
        try:
            # Declare the Client object to receive:
            Clientobject = Client()
            # Answer is calculated and serialized directly
            if self.path == "GotOrder":
                # Load Clientobject from json
                Clientobject.fromJson(body)
                answer = Queuemaster.GotOrder(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            elif self.path == "GetUpdate":
                # Load Clientobject from json
                Clientobject.fromJson(body)
                answer = Queuemaster.GetUpdate(Clientobject).toJson()
                self.send_response(200, answer)  # Send the proper response and status
            elif self.path == "Test":
                self.send_response(200,dumps("hei"))
            else:
                answer = dumps("Path Dont exist")
                self.send_response(404, dumps(answer)) #Send the proper response and status
        except TypeError:
            pass

    def do_GET(self):
        global Queuemaster
        # Only dormant server post Get:
        answer = Queuemaster.toJson()
        self.send_response(200, answer)


Handler = RequestHandler
server  = HttpServer(IP, Port, Handler)
server.serving = True

#server.Serve()


def HTTPThread():
    global Queuemaster
    RequestTimer.StartTimer()
    while True:
        if heartbeat.ServingServer:

            # Serve request:
            server.ServeOnce()
            # Check for Timeouts
            #queuemaster.CheckTimeout()

            RequestTimer.StopTimer()
            try:
                # Serve request:
                server.ServeOnce()
                # Check for Timeouts
                Queuemaster.CheckTimeout()
            except AttributeError:
                print "Error"
                pass

        else:
            if backupclient.connected and RequestTimer.GetCurrentTime() > 0.1:
                RequestTimer.StopTimer()
                temp = backupclient.GetRequest()
                RequestTimer.StartTimer()
                if temp:
                    Queuemaster = backupclient.GetRequest()


def UDPThread():
    while True:
        global backupclient
        if heartbeat.ServingServer:
            heartbeat.Heartbeat()
        else:
            heartbeat.ServerListen()
            if heartbeat.ServingServer:
                backupclient.connected = False

            elif not backupclient.connected and not heartbeat.ServingServer:
                # Bind the Client to the Ip and port of current serving server:
                Mutex.acquire()
                backupclient = HttpClient(heartbeat.ServerAdress, Port)
                Mutex.release()
                backupclient.connected = True


def MainThread():
    Thread1 = Thread(target=HTTPThread, args=(), )
    Thread2 = Thread(target=UDPThread, args=(), )
    Thread1.daemon = True
    Thread2.daemon = True
    Thread2.start()
    Thread1.start()
    print "Server Starting up..."
    while True:
        pass





# several request Works fine, handler and server coping good, need only 2 threads!:


MainThread()





