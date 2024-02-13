import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

groupList = {}

while True:
    message = json.loads(socket.recv_json())

    if message['type'] == 'group':
        if message['name'] not in groupList:
            groupList[message['name']] = message['ip']
            socket.send(b'SUCCESS')
        else:
            socket.send(b'FAIL')
        print(f"JOIN REQUEST FROM {message['ip']}")
    elif message['type'] == 'user':
        print(f"GROUP LIST REQUEST FROM {message['uuid']}")
        socket.send_json(json.dumps(groupList))