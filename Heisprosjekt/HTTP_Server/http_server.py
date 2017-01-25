
import SimpleHTTPServer
import SocketServer


http_ip="127.0.0.1"
port = 20002
handler = SimpleHTTPServer.SimpleHTTPRequestHandler


server = SocketServer.TCPServer((http_ip,port),handler)
print "serving at port", port

server.serve_forever()





