
import json
IP="192.0.255.0"
PORT=20000
adress=(IP,PORT)
data = ["im alive",adress]
#data="hei"
json1=json.dumps(data)

print json1

message=json.loads(json1)

print message[1][0]


