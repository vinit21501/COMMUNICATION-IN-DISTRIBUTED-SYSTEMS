import zmq
import json
from datetime import datetime

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
ip = input('Enter ip:port: ')
body = {
    'type' : 'group',
    'ip' : ip,
    'name' : 'shub'
}

socket.send_json(json.dumps(body))
message = socket.recv()
print(message.decode())

userList = set()
groupMessage = {}

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:" + body['ip'].split(":")[1])

def checkCredentials(socket, message, userList):
    if message['uuid'] in userList:
        return True
    else:
        return False

while True:
    message = json.loads(socket.recv_json())
    if message['request'] == 'join':
        if not checkCredentials(socket, message, userList):
            userList.add(message['uuid'])
            socket.send(b'SUCCESSS')
        else:
            socket.send(b'FAIL')
        print(f"JOIN REQUEST FROM {message['uuid']}")
    elif message['request'] == 'leave':
        if checkCredentials(socket, message, userList):
            userList.remove(message['uuid'])
            socket.send(b'SUCCESSS')
        else:
            socket.send(b'FAIL')
        print(f"LEAVE REQUEST FROM {message['uuid']}")
    elif message['request'] == 'send':
        if checkCredentials(socket, message, userList):
            groupMessage[datetime.now().timestamp()] = message['uuid'] + " -> "  + message['message']
            socket.send(b'SUCCESSS')
        else:
            socket.send(b'FAIL')
        print(f"MESSAGE SEND FROM {message['uuid']}")
    elif message['request'] == 'get':
        if checkCredentials(socket, message, userList):
            if message['time'] == '':
                socket.send_json(json.dumps(groupMessage))
            else:
                data = dict(filter(lambda x : x[0] >= message['time'], groupMessage.items()))
                socket.send_json(json.dumps(data))
        print(f"MESSAGE REQUEST FROM {message['uuid']}")
    else:
        socket.send(b'FAIL')