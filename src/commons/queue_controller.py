import pika
from pika import exceptions
import os,sys
import time
sys.path.insert(1, '../')
from commons.task import Task
from commons.cancel_request import CancelRequest
from commons.service_types import Service

RABBITURL = os.getenv('RABBITURL', "localhost")


def subscribeToQueue(callback, queue_name: str, connection=None, channel=None):
    print(f'Attempting to subscribe to {queue_name} queue...')
    con, chn = __setConChn(connection, channel)

    chn.queue_declare(queue=queue_name, durable=True)
    chn.basic_qos(prefetch_count=1)
    chn.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f'Subscribed to {queue_name} queue...')

    return con, chn


def subscribeToFanout(callback, exchange_name: str, queue_name: str = None, connection=None, channel=None):
    print(f'Attempting to subscribe to {queue_name} fanout queue...')
    con, chn = __setConChn(connection, channel)

    chn.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    if queue_name:
        result = chn.queue_declare(queue=queue_name, durable=True)
    else:
        result = chn.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    chn.queue_bind(exchange=exchange_name, queue=queue_name)
    chn.basic_consume(queue=queue_name, on_message_callback=callback)
    print(f'Subscribed to {exchange_name} fanout exchange...')

    return con, chn


# returns False if request is made as non-blocking and there's no node available to service the request
# otherwise returns the response
def requestFromQueue(queue_name: str, corr_id: str, blocking: bool = True, connection=None, channel=None):
    print(f'Attempting to make a request from {queue_name} queue...')
    con, chn = __setConChn(connection, channel)

    if not blocking:
        queue_state = chn.queue_declare(queue=queue_name, durable=True)
        if queue_state.method.consumer_count == 0:
            print(f"No nodes listening to {queue_name}. Request failed...")
            con.close()
            return False

    print(f"Sending a request to {queue_name}...")
    chn.queue_declare(queue=queue_name, durable=True)
    result = chn.queue_declare(queue='', exclusive=True)

    callback_queue = result.method.queue
    response = None

    def on_response(ch, method, props, body):
        if corr_id == props.correlation_id:
            nonlocal response
            response = body

    chn.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True)

    chn.basic_publish(
        exchange='',
        routing_key=queue_name,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id),
        body=bytes())
    print("Awaiting response...")
    while response is None:
        con.process_data_events()

    con.close()
    return response


def sendTaskToQueue(task: Task, target_queue: str):
    print(f'Attempting to send a task to {target_queue} queue...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
    channel = connection.channel()

    channel.queue_declare(queue=target_queue, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=target_queue,
        body=task.toJsonS(),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()


def sendCancelRequest(cancel_request: CancelRequest, corr_id: str, service: Service):
    print(f'Attempting to send a cancel request ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
    channel = connection.channel()
    exchange = ""
    if service == Service.PREDICTION:
        exchange = "cancellations_p"
    elif service == Service.TRAINING:
        exchange = "cancellations_t"

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    channel.basic_publish(exchange=exchange,
                          properties=pika.BasicProperties(correlation_id=corr_id),
                          routing_key='',
                          body=cancel_request.toJsonS())
    connection.close()


def __setConChn(connection, channel):
    if connection:
        con = connection
    else:
        while True:
            try:
                print("Attempting to connect to RabbitMQ")
                con = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
                break

            except exceptions.ConnectionClosedByBroker as err:
                print(f"Caught a channel error: {err}, stopping...")
                break

            except exceptions.AMQPConnectionError:
                print(f"Caught an AMQPConnection error. Connection was closed...")
                time.sleep(5)
                print("Retrying...")
                continue

    if channel:
        chn = channel
    else:
        chn = con.channel()

    return con, chn
