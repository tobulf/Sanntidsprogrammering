import socket
import sys


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_adress=('127.0.0.1', 10004)

client.connect(server_adress)
try:
    msg=client.recv(16)
    #send data
    message='Dette fungerer!'
    client.sendall(message)
    #look for response
    received=0
    expected=len(message)
    while received < expected:
        print "receiving..."
        data=client.recv(16)
        received+=len(data)

finally:
    print "closing socket"
    client.close()