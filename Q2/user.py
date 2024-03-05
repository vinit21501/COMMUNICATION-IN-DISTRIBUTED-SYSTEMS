import zmq
import json
import uuid
from datetime import datetime, timezone

body = {
    'type':'user',
    'uuid': str(uuid.uuid1())
}

class MessageServerCommunication:
    def __init__(self, ip):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(ip)
    def getGroupList(self):
        self.socket.send_json(json.dumps(body))
        return json.loads(self.socket.recv_json())

class MessageGroupCommunication:
    def __init__(self, messageServerIP):
        self.message = {
            'request' : '',
            'uuid' : body['uuid'],
            'time ' : '',
            'message' : ''
        }
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://' + messageServerIP)
    def joinGroup(self):
        self.message['request'] = 'join'
        self.socket.send_json(json.dumps(self.message))
        return self.socket.recv().decode()
    def leaveGroup(self):
        self.message['request'] = 'leave'
        self.socket.send_json(json.dumps(self.message))
        return self.socket.recv().decode()
    def getMessage(self):
        self.message['request'] = 'get'
        time = input('Provide the date time "%Y-%m-%d %H:%M:%S" (UTC): ')
        if time != '':
            dt = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            dt = dt.replace(tzinfo=timezone.utc).timestamp()
            self.message['time'] = dt
        else:
            self.message['time'] = ''
        self.socket.send_json(json.dumps(self.message))
        return json.loads(self.socket.recv_json())
    def sendMessage(self):
        self.message['request'] = 'send'
        self.message['message'] = input('Type one line message: ')
        self.socket.send_json(json.dumps(self.message))
        return self.socket.recv().decode()

if __name__ == '__main__':
    server = MessageServerCommunication("tcp://localhost:5555")
    joinedGroup = {}
    groupList = {}
    while True:
        print('1. Get Group List')
        print('2. Join Group')
        print('3. Get Message')
        print('4. Send Message')
        print('5. Close')
        option = input('Enter choice: ')
        if not option.isdigit():
            print('Please enter valid option')
            continue
        option = int(option)
        if option == 1:
            groupList = server.getGroupList()
            print('-' * 50)
            for name, ip in groupList.items():
                print(f'{name} - {ip}')
            print('-' * 50)
        elif option == 2:
            name = input('Enter the group name: ')
            if name in groupList.keys():
                joinedGroup[name] = MessageGroupCommunication(groupList[name])
                print(joinedGroup[name].joinGroup())
            else:
                print('Group IP is not present, taken from server')
        elif option == 3:
            name = input('Enter the group name: ')
            if name in joinedGroup.keys():
                message = joinedGroup[name].getMessage()
                print('-' * 50)
                for time, mess in message.items():
                    print(f"{str(datetime.fromtimestamp(float(time))) } : {mess}")
                print('-' * 50)
            else:
                print('Group is not joined')
        elif option == 4:
            name = input('Enter the group name: ')
            if name in joinedGroup.keys():
                print(joinedGroup[name].sendMessage())
            else:
                print('Group is not joined')
        elif option == 5:
            break
        else:
            print('Please enter valid option')