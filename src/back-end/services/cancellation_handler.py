from uuid import UUID, uuid4
import os
import pika
import jsonpickle

if "RABBITURL" in os.environ:
    RABBITURL = os.environ["RABBITURL"]
else:
    RABBITURL = "localhost"


class CancellationHandler(object):

    def __init__(self):
        self.__current_task: UUID = UUID("00000000-0000-0000-0000-000000000000")
        self.__cancelSet: set = set()
        self.corr_id = str(uuid4())

    def getCurrentTask(self):
        return self.__current_task

    def setCurrentTask(self, taskID: UUID):
        self.__current_task = taskID

    def addCancel(self, taskID: UUID, persist=False):
        self.__cancelSet.add(taskID)
        if persist:
            self.__persistCancelSet()

    def hasCancel(self, taskID: UUID):
        return taskID in self.__cancelSet

    def removeCancel(self, taskID: UUID, persist=False):
        self.__cancelSet.discard(taskID)
        if persist:
            self.__persistCancelSet()

    def getAllCancelPickled(self):
        return jsonpickle.encode(self.__cancelSet)

    def isEmpty(self):
        return len(self.__cancelSet) == 0

    # get state from network blocks until it receives a cancel set
    # no worker should start if it's unable to receive a cancel set from the persistence node
    def getStateFromNetwork(self, blocking=True, persist=False):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITURL))
        channel = connection.channel()

        # check if any nodes are available to ask for state of cancel set
        # if not, then initialise cancel set to empty
        if not blocking:
            queue_state = channel.queue_declare(queue="cancel_set_request", passive=True, durable=True)
            if queue_state.method.consumer_count == 0:
                print("Did not find a node to request cancel set state from.")
                connection.close()
                return False

        print("Requesting cancel set state...")
        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        response = None

        def on_response(ch, method, props, body):
            if self.corr_id == props.correlation_id:
                nonlocal response
                response = body

        channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

        channel.basic_publish(
            exchange='',
            routing_key="cancel_set_request",
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=self.corr_id),
            body=bytes())
        while response is None:
            connection.process_data_events()

        response_decoded = jsonpickle.decode(response)
        self.__cancelSet = response_decoded
        print(f"Initialised cancel set from network to: {self.__cancelSet}")
        connection.close()

        if persist:
            self.__persistCancelSet()

        return True

    def getStateFromDisk(self):
        if not os.path.isfile("../persistence/cancel_set"):
            print("Cancel_set file not found. Setting cancel_set persistence file to empty...")
            return

        with open("../persistence/cancel_set", "r") as infile:
            encoded_set = infile.read()
            self.__cancelSet = jsonpickle.decode(encoded_set)

        print(f"Persistent cancel_set initialised from disk to: {self.__cancelSet}")

    def __persistCancelSet(self):
        with open("../persistence/cancel_set", "w+") as outfile:
            outfile.write(jsonpickle.encode(self.__cancelSet))
        print(f"Persisted cancel_set state as: {self.__cancelSet}")
