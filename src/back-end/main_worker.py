from uuid import UUID
import pika

from services.cancel_request import CancelRequest
from services.cancellation_handler import CancellationHandler
from services.queue_controller import subscribeToRabbit, ThreadedWorkerConsumer

cancellations: CancellationHandler = CancellationHandler()


def cancel_callback(ch, method, properties, body):
    # check if the node is not receiving a message from itself
    if properties.correlation_id == cancellations.corr_id:
        return

    req = CancelRequest.fromJsonS(body.decode())
    taskID: UUID = req.taskID
    was_cancelled: bool = req.cancelled

    # another worker has cancelled this task, remove it from cancel set
    if was_cancelled and cancellations.hasCancel(taskID):
        cancellations.removeCancel(taskID)
        print(f"Another node cancelled task with ID {taskID}. Removed it from the cancel set.")

    # the node is currently working on this task. Tell it to stop and have it perform cleanup.
    elif taskID == cancellations.getCurrentTask():
        td.cancelTask()

    # the task is in the queue or at another worker node. Add its id to cancel set
    else:
        cancellations.addCancel(taskID)
        print(f"Received request to cancel task with ID {taskID}. Added its ID to cancel set.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def cancel_set_request_callback(ch, method, properties, body):
    response = cancellations.getAllCancelPickled()

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                     body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    td = ThreadedWorkerConsumer(cancellations)

    subscribeToRabbit(cancel_callback, cancel_set_request_callback, cancellations, td)
