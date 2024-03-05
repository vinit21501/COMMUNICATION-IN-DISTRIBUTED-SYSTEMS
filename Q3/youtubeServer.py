import sys
import pika
import json
import os

youtuberList = set()
userList = set()
subscriptionList = {}

def notify_users(ch, body):
    data = json.loads(body)
    print('new video is uploaded')
    for user in subscriptionList[data['youtuber']]:
        # print(f"{user} have {data}")
        ch.queue_declare(queue=user)
        ch.basic_publish(exchange='', routing_key=user, body=body)

def consume_user_requests(ch, method, properties, body):
    data = json.loads(body)
    if data['youtuber'] not in subscriptionList:
        subscriptionList[data['youtuber']] = set()
    if data['subscribe']:
        print(f"{data['user']} subscribted {data['youtuber']}")
        subscriptionList[data['youtuber']].add(data['user'])
    else:
        if data['user'] in subscriptionList[data['youtuber']]:
            print(f"{data['user']} unsubscribted {data['youtuber']}")
            subscriptionList[data['youtuber']].remove(data['user'])
        else:
            print(f"{data['user']} not subscribted {data['youtuber']}")
    

def consume_youtuber_requests(ch, method, properties, body):
    data = json.loads(body)
    youtuberList.add(data['youtuber'])
    if data['youtuber'] not in subscriptionList:
        subscriptionList[data['youtuber']] = set()
    notify_users(ch, body)
    print("SUCCESS")

def serve():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='uploadvideo')
    channel.queue_declare(queue='userRequest')

    channel.basic_consume(queue='uploadvideo', on_message_callback=consume_youtuber_requests, auto_ack=True)
    channel.basic_consume(queue='userRequest', on_message_callback=consume_user_requests, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        serve()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)