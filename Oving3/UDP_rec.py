import socket 


UDP_IP = "127.0.0.1"
UDP_PORT = 20010



client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #setting up a Instance of socket. with IP4 and
client.bind((UDP_IP,UDP_PORT))

while True:
	data1, addr=client.recvfrom(1024) #buffersize

	print "received data:", data1