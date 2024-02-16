import sys
import pika
import json

def publishVideo(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
            # ,credentials=pika.PlainCredentials('vinit', 'vinit1june')
            ))
    channel = connection.channel()
    channel.queue_declare(queue='uploadvideo')
    
    channel.basic_publish(exchange='', routing_key='uploadvideo', body=json.dumps(body))
    connection.close()

def run():
    argc = len(sys.argv)
    argv = sys.argv
    if argc <= 1:
        print('Please give some arguments for\nsubscribe, unsubscribe to a YouTuber, and receive notifications')
    if argc > 2:
        body = {'youtuber' : argv[1], 'video' : ' '.join(argv[2:])}
        publishVideo(body)
    else:
        print('invalid arguments')

if __name__ == '__main__':
    try:
        run()
    except:
        print('interrupt')