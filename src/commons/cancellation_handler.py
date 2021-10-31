from uuid import UUID, uuid4
import os
from pathlib import Path
import jsonpickle
from commons.queue_controller import requestFromQueue
from commons.service_types import Service


class CancellationHandler(object):

    def __init__(self, service: Service):
        self.__current_task: UUID = UUID(
            "00000000-0000-0000-0000-000000000000")
        self.__cancelSet: set = set()
        self.corr_id = str(uuid4())
        self.service_type: Service = service
        Path("../persistence").mkdir(exist_ok=True, parents=True)

    def getCurrentTask(self):
        return self.__current_task

    def setCurrentTask(self, taskID: UUID):
        self.__current_task = taskID

    def addCancel(self, taskID: UUID, persist: bool = False):
        self.__cancelSet.add(taskID)
        if persist:
            self.__persistCancelSet()

    def hasCancel(self, taskID: UUID):
        return taskID in self.__cancelSet

    def removeCancel(self, taskID: UUID, persist: bool = False):
        self.__cancelSet.discard(taskID)
        if persist:
            self.__persistCancelSet()

    def getAllCancelPickled(self):
        return jsonpickle.encode(self.__cancelSet)

    def isEmpty(self):
        return len(self.__cancelSet) == 0

    # get state from network blocks until it receives a cancel set
    # no worker should start if it's unable to receive a cancel set from the
    # persistence node
    def getStateFromNetwork(self, blocking: bool = True,
                            persist: bool = False):

        if self.service_type == Service.PREDICTION:
            queue_name = "cancel_set_request_p"
        elif self.service_type == Service.TRAINING:
            queue_name = "cancel_set_request_t"
        else:
            queue_name = "erroneous queue"

        response = requestFromQueue(queue_name, self.corr_id, blocking)

        if not response:
            return False

        response_decoded = jsonpickle.decode(response)
        self.__cancelSet = response_decoded
        print(f"Initialised cancel set from network to: {self.__cancelSet}")

        if persist:
            self.__persistCancelSet()

        return True

    def getStateFromDisk(self):
        if not os.path.isfile(self.__getPath()):
            print(
                "cancel_set file not found. Setting cancel_set persistence file to empty...")
            return

        with open(self.__getPath(), "r") as infile:
            encoded_set = infile.read()
            self.__cancelSet = jsonpickle.decode(encoded_set)

        print(
            f"Persistent cancel_set initialised from disk to: {self.__cancelSet}")

    def __persistCancelSet(self):
        with open(self.__getPath(), "w+") as outfile:
            outfile.write(jsonpickle.encode(self.__cancelSet))
        print(f"Persisted cancel_set state as: {self.__cancelSet}")

    def __getPath(self):
        if self.service_type == Service.PREDICTION:
            return "../persistence/cancel_set_p"
        elif self.service_type == Service.TRAINING:
            return "../persistence/cancel_set_t"
