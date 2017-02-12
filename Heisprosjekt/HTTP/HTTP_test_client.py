from HTTP_driver import HttpClient
address =""
port = 20010

client = HttpClient(adress,port)
message = ["this shit works!!!"]
path = ""
response = client.PostRequest(path,message)
print response[0]
