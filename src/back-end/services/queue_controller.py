import pika
import threading
import time
import os

from services.cancel_request import CancelRequest
from services.cancellation_handler import CancellationHandler
from services.task import Task
from services.task_manager import TaskManager

if "RABBITURL" in os.environ:
    RABBITURL = os.environ["RABBITURL"]
else:
    RABBITURL = "localhost"


def sendTaskToQueue(task: Task, target_queue: str):
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


def sendCancelRequest(cancel_request: CancelRequest):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
    channel = connection.channel()

    channel.exchange_declare(exchange='cancellations', exchange_type='fanout')

    channel.basic_publish(exchange='cancellations', routing_key='', body=cancel_request.toJsonS())

    connection.close()


# def subscribeToInputQueue():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
#     channel = connection.channel()
#
#     channel.queue_declare(queue="input", durable=True)
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue="input", on_message_callback=worker_callback)
#
#     print("Consuming events from RabbitMQ input queue...")
#     channel.start_consuming()


def subscribeToCancelQueue(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
    channel = connection.channel()

    channel.exchange_declare(exchange='cancellations', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='cancellations', queue=queue_name)

    print('Subscribed to Cancellations exchange...')

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback)

    channel.start_consuming()


# def worker_callback(channel, method, properties, body):
#     received_task = Task.fromJsonS(body.decode())
#     print(f"Received task: {received_task.toJsonS()}")
#     # start fake-processing task and let the master node know about that
#     received_task.setStatus(Task.Status.PROCESSING)
#     print(f"Began processing task: {received_task.taskID}")
#     sendTaskToQueue(received_task, "output")
#
#     time.sleep(30)
#
#     received_task.setStatus(Task.Status.COMPLETED)
#     print(f"Finished processing task: {received_task.taskID}")
#     sendTaskToQueue(received_task, "output")
#     os.remove(received_task.monitor_path)
#     os.remove(received_task.event_log_path)
#     channel.basic_ack(delivery_tag=method.delivery_tag)


# Thread used by the worker node to listen for task requests
class ThreadedWorkerConsumer(threading.Thread):
    def __init__(self, cancellations: CancellationHandler):
        self.cancellations = cancellations
        self.cancel_flag = False
        threading.Thread.__init__(self)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
        self.channel = connection.channel()

        self.channel.queue_declare(queue="input", durable=True)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="input", on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        self.cancel_flag = False
        received_task = Task.fromJsonS(body.decode())

        if self.cancellations.hasCancel(received_task.taskID):
            self.cancellations.removeCancel(received_task.taskID)

            os.remove(received_task.monitor_path)
            os.remove(received_task.event_log_path)

            print(f"Task with ID: {received_task.taskID} present in cancel set.\n"
                  f"Removed files corresponding to the task.")

            sendCancelRequest(CancelRequest(received_task.taskID, True))
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            self.cancellations.setCurrentTask(received_task.taskID)
            print(f"Received task: {received_task.toJsonS()}")
            # start fake-processing task and let the master node know about that
            received_task.setStatus(Task.Status.PROCESSING)
            print(f"Began processing task: {received_task.taskID}")
            sendTaskToQueue(received_task, "output")

            for _ in range(30):
                time.sleep(1)
                if self.cancel_flag:
                    received_task.setStatus(Task.Status.CANCELLED)
                    os.remove(received_task.monitor_path)
                    os.remove(received_task.event_log_path)
                    sendCancelRequest(CancelRequest(received_task.taskID, True))
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    print(f"Cancelled current task with ID: {received_task.taskID}.")
                    return

            received_task.setStatus(Task.Status.COMPLETED)
            print(f"Finished processing task: {received_task.taskID}")
            sendTaskToQueue(received_task, "output")
            os.remove(received_task.monitor_path)
            os.remove(received_task.event_log_path)
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print("Consuming events from RabbitMQ input queue...")
        self.channel.start_consuming()

    def stop(self):
        self.cancel_flag = True


# Thread used by master node to listen for progress on tasks
class ThreadedMasterConsumer(threading.Thread):
    def __init__(self, tasks: TaskManager):
        self.tasks = tasks
        threading.Thread.__init__(self)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
        self.channel = connection.channel()

        self.channel.queue_declare(queue="output", durable=True)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue="output", on_message_callback=self.callback)

    def callback(self, channel, method, properties, body):
        received_task = Task.fromJsonS(body.decode())
        self.tasks.updateTask(received_task)
        print(f"Set status of task {received_task.taskID} to: {received_task.status}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print("Consuming events from RabbitMQ output queue...")
        self.channel.start_consuming()
