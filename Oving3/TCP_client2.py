import socket



TCP_IP="129.241.187.158"
TCP_PORT=34550

data = "halla bro \0"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((TCP_IP, TCP_PORT))
    received = sock.recv(1024)
    print received
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)