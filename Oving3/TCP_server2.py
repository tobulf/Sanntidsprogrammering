import socket
import SocketServer




TCP_IP="129.241.187.158"
TCP_PORT=34550


#server=SocketServer.TCPServer((TCP_IP,TCP_PORT), )


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.sendall("Hello, you are connect to:"+TCP_IP)
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        if ("\0" in self.data):
            self.request.sendall(("received: ")+self.data)


# Create the server, binding to localhost on port 9999
server = SocketServer.TCPServer((TCP_IP, TCP_PORT), MyTCPHandler)

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
server.serve_forever()
