import threading
import time
from socket import gaierror
from pika import exceptions
from commons.task import Task
from commons.task_manager import TaskManager
from src.commons.queue_controller import subscribeToQueue, sendTaskToQueue


class MasterConsumerThread(threading.Thread):
    def __init__(self, tasks: TaskManager):
        self.tasks = tasks
        threading.Thread.__init__(self)

    def callback(self, channel, method, properties, body):
        received_task = Task.fromJsonS(body.decode())
        self.tasks.updateTask(received_task)
        sendTaskToQueue(received_task, "persistent_task_status")
        print(f"Set status of task {received_task.taskID} to: {received_task.status}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        print("Starting master node's consumer thread...")
        while True:
            try:
                con, chn = subscribeToQueue(self.callback, "output")
                chn.start_consuming()

            except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
                print(f"Consumer thread caught the following error when attempting to reconnect to RabbitMQ: {err}")
                time.sleep(5)
                print("Retrying...")
                continue
