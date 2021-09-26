import multiprocessing as mp
import os
import shutil
import sys
import threading
import time
from commons.cancellation_handler import CancellationHandler
from commons.cancel_request import CancelRequest
from commons.nirdizati_wrapper import predict, train
from commons.queue_controller import subscribeToQueue, sendCancelRequest, sendTaskToQueue
from commons.task import Task
import commons.file_handler as fh


class WorkerConsumerThread(threading.Thread):
    def __init__(self, cancellations: CancellationHandler):
        self.cancellations = cancellations
        self.cancel_flag = False
        threading.Thread.__init__(self)

        self.con, self.chn = subscribeToQueue(self.callback, "input")

        # Setup environment
        env_dir = "../nirdizati-training-backend"
        os.environ["PYTHONPATH"] = env_dir
        sys.path.append(env_dir)

    def callback(self, channel, method, properties, body):
        self.cancel_flag = False
        received_task = Task.fromJsonS(body.decode())

        if self.cancellations.hasCancel(received_task.taskID):
            self.cancellations.removeCancel(received_task.taskID)

            # TRAINING/PREDICTION SPLIT
            if received_task.predictors_path:
                fh.removePredictTaskFile(received_task.taskID)
            else:
                fh.removeTrainingTaskFile(received_task.taskID)

            print(f"Task with ID: {received_task.taskID} present in cancel set.\n"
                  f"Removed files corresponding to the task.\n"
                  f"Waiting for a new task...")

            sendCancelRequest(CancelRequest(received_task.taskID, True), self.cancellations.corr_id)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        else:
            self.cancellations.setCurrentTask(received_task.taskID)
            print(f"Received task: {received_task.toJsonS()}")
            received_task.setStatus(Task.Status.PROCESSING)
            print(f"Began processing task: {received_task.taskID}")
            sendTaskToQueue(received_task, "output")

            predictor_abs = os.path.join(os.getcwd(), received_task.predictors_path)
            config_abs = os.path.join(os.getcwd(), received_task.config_path)
            schema_abs = os.path.join(os.getcwd(), received_task.schema_path)
            eventlog_abs = os.path.join(os.getcwd(), received_task.event_log_path)
            prediction_output_abs = os.path.join(os.getcwd(), fh.loadPredictRoot(received_task.taskID), received_task.taskID)
            training_output_abs = os.path.join(os.getcwd(), fh.loadTrainingRoot(received_task.taskID), received_task.taskID)
            
            # TRAINING/PREDICTION SPLIT
            if received_task.predictors_path:
                p = mp.Process(target=predict, args=(predictor_abs, eventlog_abs, prediction_output_abs))
            else:
                p = mp.Process(target=train, args=(config_abs, schema_abs, eventlog_abs, training_output_abs))

            p.start()

            # todo: we're missing an error handler in case the prediction process throws an error
            while True:
                time.sleep(1)

                # Task is cancelled
                if self.cancel_flag:
                    p.kill()
                    while p.is_alive():
                        time.sleep(0.1)
                    received_task.setStatus(Task.Status.CANCELLED)

                    # TRAINING/PREDICTION SPLIT
                    if received_task.predictors_path:
                        fh.removePredictTaskFile(received_task.taskID)
                    else:
                        fh.removeTrainingTaskFile(received_task.taskID)
                    
                    sendCancelRequest(CancelRequest(received_task.taskID, True), self.cancellations.corr_id)
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    print(f"Cancelled current task with ID: {received_task.taskID}.")
                    return

                # Processing is finished
                elif not p.is_alive():
                    p.close()
                    received_task.setStatus(Task.Status.COMPLETED)
                    print(f"Finished processing task: {received_task.taskID}")
                    sendTaskToQueue(received_task, "output")
                    
                    try:
                        os.remove(received_task.schema_path)
                        os.remove(received_task.event_log_path)
                        # TRAINING/PREDICTION SPLIT
                        if received_task.predictors_path:
                            shutil.rmtree(received_task.predictors_path, onerror = lambda func, path, excinfo : print(excinfo))
                        else:
                            fh.zipFile(received_task.taskID, keep_files = False)
                    except OSError as err:
                        print(err)

                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    print("Waiting for a new task...")
                    return

                else:
                    print(f"Currently processing task: {received_task.taskID}")

    def run(self):
        print("Consuming events from RabbitMQ input queue...")
        self.chn.start_consuming()

    def cancelTask(self):
        self.cancel_flag = True
