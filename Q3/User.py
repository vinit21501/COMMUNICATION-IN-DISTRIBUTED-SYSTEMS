import sys
import pika
import json
import os

def updateSubscription(ch, body):
    ch.queue_declare(queue='userRequest')
    ch.basic_publish(exchange='', routing_key='userRequest', body=json.dumps(body))
    print(f"{body['user']} subscription/unsubscription request {body['youtuber']}")

def printMessage(ch, method, properties, body):
    data = json.loads(body)
    print(f"New Notification: '{data['youtuber']}' uploaded '{data['video']}'")

def receiveNotifications(ch, userName):
    qname = userName
    ch.queue_declare(queue=qname)
    ch.basic_consume(queue=qname, on_message_callback=printMessage, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    ch.start_consuming()

def run():
    argc = len(sys.argv)
    argv = sys.argv
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
            # ,credentials=pika.PlainCredentials('vinit', 'vinit1june')
            ))
    channel = connection.channel()
    if argc <= 1:
        print('Please give some arguments for\nsubscribe, unsubscribe to a YouTuber, and receive notifications')
        return
    userName = argv[1]
    if argc == 2:
        receiveNotifications(channel, userName)
    elif argc > 2:
        if argv[2] == 'u' or argv[2] == 'U':
            body = {
                "user": userName,
                "youtuber": argv[3],
                "subscribe": False
                }
            updateSubscription(channel, body)
            receiveNotifications(channel, userName)
        elif argv[2] == 's' or argv[2] == 'S':
            body = {
                "user": userName,
                "youtuber": argv[3],
                "subscribe": True
                }
            updateSubscription(channel, body)
            receiveNotifications(channel, userName)
        else:
            print('invalid arguments')
    else:
        print('invalid arguments')
    connection.close()
    

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)