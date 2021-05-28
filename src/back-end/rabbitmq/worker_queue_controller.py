#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from Task import Task
import pika
import json


def pushTask(task: Task):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    routing_key = 'anonymous.info'

    message = json.dumps(task, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    channel.basic_publish(
        exchange='topic_logs', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()


def popTask():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = 'anonymous.info'

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    # print(' [*] Waiting for logs. To exit press CTRL+C')

    json_str = channel.consume(queue_name).body
    connection.cloes()
    return json.loads(json_str)


def check(taskID: Task):
    return "OK"
