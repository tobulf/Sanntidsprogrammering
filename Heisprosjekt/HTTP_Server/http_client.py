import httplib



port=20002
http_ip="127.0.0.1"

connection=httplib.HTTPSConnection(http_ip,port)
connection.connect()
connection.putrequest("do_GET()")
r1=connection.getresponse()
print r1.status



