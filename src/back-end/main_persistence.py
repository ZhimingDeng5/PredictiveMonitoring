from services.cancellation_handler import CancellationHandler
from services.queue_controller import subscribeToQueue, subscribeToFanout
from services.cancel_request import CancelRequest
from services.task_manager import TaskManager
from services.task import Task
import pika
from uuid import UUID


class PersistenceNode:

    def __init__(self):
        print("Creating persistence node...")
        self.__cancellations: CancellationHandler = CancellationHandler()
        self.__cancellations.getStateFromDisk()

        self.__tasks: TaskManager = TaskManager()
        self.__tasks.getStateFromDisk()

    def start(self):
        print("Starting persistence node...")

        def cancel_callback(ch, method, properties, body):
            req = CancelRequest.fromJsonS(body.decode())
            taskID: UUID = req.taskID
            was_cancelled: bool = req.cancelled

            # if receiving a message saying a node has cancelled the task
            if was_cancelled:
                print(f"Another node cancelled task with id: {taskID}. Removing it from cancel set.")
                self.__cancellations.removeCancel(taskID, True)
            # if receiving a message that the task is meant to be cancelled
            else:
                print(f"Received a request to cancel task with id: {taskID}. Adding it to cancel set.")
                self.__cancellations.addCancel(taskID, True)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        def set_request_callback(ch, method, properties, body):
            response = self.__cancellations.getAllCancelPickled()

            ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                             body=response)

            print(f"Responded to request for cancel set with {response}...")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        def task_callback(ch, method, properties, body):
            if body == bytes():
                response = self.__tasks.getAllTasksPickled()

                ch.basic_publish(exchange='',
                                 routing_key=properties.reply_to,
                                 properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                                 body=response)

                print(f"Responded to request for task status with {response}...")

            else:
                received_task: Task = Task.fromJsonS(body.decode())

                if received_task.status == Task.Status.CANCELLED.name:
                    print(f"Removing task: {received_task}...")
                    self.__tasks.removeTask(received_task.taskID, True)

                else:
                    print(f"Updating and persisting task: {received_task}...")
                    self.__tasks.updateTask(received_task, True)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        con, chn = subscribeToFanout(cancel_callback, 'cancellations', 'persistent_cancel_queue')
        con, chn = subscribeToQueue(set_request_callback, 'cancel_set_request', con, chn)
        con, chn = subscribeToQueue(task_callback, 'persistent_task_status', con, chn)
        chn.start_consuming()


if __name__ == '__main__':
    persistence_node = PersistenceNode()
    persistence_node.start()
