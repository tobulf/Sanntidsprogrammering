import BaseHTTPServer




server_ip="127.0.0.1"
server_port= 20001

handler=BaseHTTPServer.BaseHTTPRequestHandler
server=BaseHTTPServer.HTTPServer(server_ip,handler)
