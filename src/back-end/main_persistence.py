from services.cancellation_handler import CancellationHandler
from services.cancellation_handler import RABBITURL
from services.cancel_request import CancelRequest
import pika
from uuid import UUID


class PersistenceNode:

    def __init__(self):
        self.__cancellations: CancellationHandler = CancellationHandler()

        if not self.__cancellations.getStateFromNetwork(blocking=False, persist=True):
            self.__cancellations.getStateFromDisk()

    def start(self):

        def cancel_callback(ch, method, properties, body):
            req = CancelRequest.fromJsonS(body.decode())
            taskID: UUID = req.taskID
            was_cancelled: bool = req.cancelled

            # if receiving a message saying a node has cancelled the task
            if was_cancelled:
                self.__cancellations.removeCancel(taskID, True)
            # if receiving a message that the task is meant to be cancelled
            else:
                self.__cancellations.addCancel(taskID, True)

        def set_request_callback(ch, method, properties, body):
            response = self.__cancellations.getAllCancelPickled()

            ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                             body=response)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
        channel = connection.channel()

        channel.exchange_declare(exchange='cancellations', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='cancellations', queue=queue_name)
        channel.basic_consume(
            queue=queue_name, on_message_callback=cancel_callback)
        print('Persistence node monitoring cancellations exchange...')

        channel.queue_declare(queue='cancel_set_request', durable=True)
        channel.basic_consume(
            queue='cancel_set_request', on_message_callback=set_request_callback)
        print('Subscribed to cancel_set_request queue...')

        channel.start_consuming()


if __name__ == '__main__':
    persistence_node = PersistenceNode()
    persistence_node.start()
