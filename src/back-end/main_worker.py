from uuid import UUID

from services.cancel_request import CancelRequest
from services.cancellation_handler import CancellationHandler
from services.queue_controller import subscribeToCancelQueue, ThreadedWorkerConsumer

cancellations: CancellationHandler = CancellationHandler()


def cancel_callback(ch, method, properties, body):
    req = CancelRequest.fromJsonS(body.decode())
    taskID: UUID = req.taskID
    was_cancelled: bool = req.cancelled

    # another worker has cancelled this task, remove it from cancel set
    if was_cancelled and cancellations.hasCancel(taskID):
        cancellations.removeCancel(taskID)
        print(f"Another node cancelled task with ID {taskID}. Removed it from the cancel set.")

    # the node is currently working on this task. Stop and delete its files
    elif taskID == cancellations.getCurrentTask():
        td.stop()

    # the task is in the queue or at another worker node. Add its id to cancel set
    else:
        cancellations.addCancel(taskID)
        print(f"Received request to cancel task with ID {taskID}. Added its ID to cancel set.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    td = ThreadedWorkerConsumer(cancellations)
    td.start()

    subscribeToCancelQueue(cancel_callback)
