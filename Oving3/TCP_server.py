import socket



#Creating a TCP socket:
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#binding the socket to a specific port:
server_adress=('127.0.0.1', 10005)
sock.bind(server_adress)

#Listen for connections:
sock.listen(1)
welcome_msg=server_adress
while True:
    #wait for connection
    connection, client_adress= sock.accept()
    try:

        print "connection from",client_adress
        #send welcome msg:
        connection.sendall(welcome_msg)
        #receive data:
        while True:
            print "Looking for data"
            data=connection.recv(16) #buffersize 16
            if data:
                print"sending data"
                connection.sendall(data)
            else:
                break
    finally:
        #clean up connection
        connection.close()






