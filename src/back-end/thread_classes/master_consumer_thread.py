import threading
import time
from services.task import Task
from services.task_manager import TaskManager
from services.queue_controller import subscribeToQueue, sendTaskToQueue


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

            except Exception as err:
                print(f"Consumer thread caught the following error when attempting to reconnect to RabbitMQ: {err}")
                time.sleep(1)
                print("Retrying...")
                continue
