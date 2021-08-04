import pika
import threading
import time
import os
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


def subscribeToInputQueue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITURL))
    channel = connection.channel()

    channel.queue_declare(queue="input", durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="input", on_message_callback=worker_callback)

    print("Consuming events from RabbitMQ input queue...")
    channel.start_consuming()


# once the worker does something other than pretending to work this will get refactored to its own module
def worker_callback(channel, method, properties, body):
    received_task = Task.fromJsonS(body.decode())
    print(f"Received task: {received_task.toJsonS()}")

    # start fake-processing task and let the master node know about that
    received_task.setStatus(Task.Status.PROCESSING)
    print(f"Began processing task: {received_task.taskID}")
    sendTaskToQueue(received_task, "output")
    time.sleep(10)

    received_task.setStatus(Task.Status.COMPLETED)
    print(f"Finished processing task: {received_task.taskID}")
    sendTaskToQueue(received_task, "output")
    os.remove(received_task.monitor_path)
    os.remove(received_task.event_log_path)
    channel.basic_ack(delivery_tag=method.delivery_tag)


# Thread used by master node to listen for progress on tasks
class ThreadedConsumer(threading.Thread):
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
        self.channel.start_consuming()
        print("Consuming events from RabbitMQ output queue...")
