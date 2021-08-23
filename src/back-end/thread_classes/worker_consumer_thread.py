import threading
import os
import time
import shutil
from services.cancellation_handler import CancellationHandler
from services.cancel_request import CancelRequest
from services.queue_controller import subscribeToQueue, sendCancelRequest, sendTaskToQueue
from services.task import Task


class WorkerConsumerThread(threading.Thread):
    def __init__(self, cancellations: CancellationHandler):
        self.cancellations = cancellations
        self.cancel_flag = False
        threading.Thread.__init__(self)

        self.con, self.chn = subscribeToQueue(self.callback, "input")

    def callback(self, channel, method, properties, body):
        self.cancel_flag = False
        received_task = Task.fromJsonS(body.decode())

        if self.cancellations.hasCancel(received_task.taskID):
            self.cancellations.removeCancel(received_task.taskID)

            os.remove(received_task.monitor_path)
            os.remove(received_task.event_log_path)

            print(f"Task with ID: {received_task.taskID} present in cancel set.\n"
                  f"Removed files corresponding to the task.\n"
                  f"Waiting for a new task...")

            sendCancelRequest(CancelRequest(received_task.taskID, True), self.cancellations.corr_id)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            self.cancellations.setCurrentTask(received_task.taskID)
            print(f"Received task: {received_task.toJsonS()}")
            # start fake-processing task and let the master node know about that
            received_task.setStatus(Task.Status.PROCESSING)
            print(f"Began processing task: {received_task.taskID}")
            sendTaskToQueue(received_task, "output")

            # start generating predictions in a separate process
            # in place of the for loop put a while true loop that will check for cancel flag every x seconds
            # if cancel flag is raised terminate the prediction process started above and perform cleanup
            # if process terminates successfully break out fo the loop

            path_prefix: str = f"{os.getcwd()}\\task_files\{received_task.taskID}"

            # print(path_prefix)
            # predictions = threading.Thread(target = predict, args = (f"{path_prefix}-monitor", f"{path_prefix}-event_log", path_prefix))
            # predictions.start()

            while True:
                time.sleep(1)
                if self.cancel_flag:
                    received_task.setStatus(Task.Status.CANCELLED)
                    shutil.rmtree(received_task.monitor_path)
                    os.remove(received_task.event_log_path)
                    sendCancelRequest(CancelRequest(received_task.taskID, True), self.cancellations.corr_id)
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    print(f"Cancelled current task with ID: {received_task.taskID}.")
                    return

                # elif not predictions.is_alive():
                #     received_task.setStatus(Task.Status.COMPLETED)
                #     print(f"Finished processing task: {received_task.taskID}")
                #     sendTaskToQueue(received_task, "output")
                #     shutil.rmtree(received_task.monitor_path)
                #     os.remove(received_task.event_log_path)
                #     channel.basic_ack(delivery_tag=method.delivery_tag)
                #     print("Waiting for a new task...")
                #     return

                else:
                    print(f"Currently processing task: {received_task.taskID}")

    def run(self):
        print("Consuming events from RabbitMQ input queue...")
        self.chn.start_consuming()

    def cancelTask(self):
        self.cancel_flag = True
