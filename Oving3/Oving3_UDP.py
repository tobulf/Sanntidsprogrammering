import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 20010
MESSAGE= "Hallla, UDP funker jo!"

print "UDP target IP", UDP_IP
print "UDP target port", UDP_PORT
print "Message ", MESSAGE

sock=socket.socket(socket.AF_INET, #internet
				 socket.SOCK_DGRAM) #UDP
sock.sendto(MESSAGE, (UDP_IP,UDP_PORT))


print("works")