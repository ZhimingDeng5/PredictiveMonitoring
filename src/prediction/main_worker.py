from uuid import UUID
import sys
sys.path.insert(1, '../')
import pika
from commons.cancel_request import CancelRequest
from commons.cancellation_handler import CancellationHandler
from commons.thread_classes.worker_consumer_thread import WorkerConsumerThread
from commons.queue_controller import subscribeToQueue, subscribeToFanout
from commons.service_types import Service


class WorkerNode:
    def __init__(self):
        self.cancellations: CancellationHandler = CancellationHandler(Service.PREDICTION)
        self.cancellations.getStateFromNetwork()

        self.worker_thread = WorkerConsumerThread(self.cancellations, Service.PREDICTION)

    def start(self):

        def cancel_callback(ch, method, properties, body):
            # check if the node is not receiving a message from itself
            if properties.correlation_id == self.cancellations.corr_id:
                return

            req = CancelRequest.fromJsonS(body.decode())
            taskID: UUID = req.taskID
            was_cancelled: bool = req.cancelled

            # another worker has cancelled this task, remove it from cancel set
            if was_cancelled and self.cancellations.hasCancel(taskID):
                self.cancellations.removeCancel(taskID)
                print(f"Another node cancelled task with ID {taskID}. Removed it from the cancel set.")

            # the node is currently working on this task. Tell it to stop and have it perform cleanup.
            elif taskID == self.cancellations.getCurrentTask():
                self.worker_thread.cancelTask()

            # the task is in the queue or at another worker node. Add its id to cancel set
            else:
                self.cancellations.addCancel(taskID)
                print(f"Received request to cancel task with ID {taskID}. Added its ID to cancel set.")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        def cancel_set_request_callback(ch, method, properties, body):
            response = self.cancellations.getAllCancelPickled()

            ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                             body=response)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        con, chn = subscribeToFanout(cancel_callback, 'cancellations_p')
        con, chn = subscribeToQueue(cancel_set_request_callback, 'cancel_set_request_p', con, chn)

        self.worker_thread.start()
        chn.start_consuming()


if __name__ == '__main__':
    worker = WorkerNode()
    worker.start()
