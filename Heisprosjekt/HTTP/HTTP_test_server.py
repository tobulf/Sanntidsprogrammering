from BaseHTTPServer import BaseHTTPRequestHandler
from HTTP_driver import HttpServer
from json import dumps,loads
message=["yep it works"]
data =dumps(message)

address = "129.241.187.143"
port = 20010
class RequestHandler(BaseHTTPRequestHandler):
    # custom made handler class
    def do_POST(self):
        path = self.path
        content_len = int(self.headers.getheader('content-length', 0)) #Finding the length of the response body
        body = self.rfile.read(content_len) #Extracting the body
        messagerecv=loads(body)
        print messagerecv[0]
        #Must make a proper response function here
        self.send_response(200, data) #Send the proper response and status

handler = RequestHandler
server = HttpServer(address, port, handler)
server.serving = True

while True:
    server.Serve()

