import demjson
import json
IP="ip"
PORT=120
data = ["im alive",IP,PORT]
json1=json.dumps(data)
print json1
message = json.loads(json1)
print message[0]

