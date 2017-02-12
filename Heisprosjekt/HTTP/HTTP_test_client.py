from HTTP_driver import HttpClient
address = "129.241.187.143"
port = 20010

client = HttpClient(address,port)
client.connected = True
message = ["this shit works!!!"]
path = "Works"

response = client.PostRequest(path, message)
print response[0]
