from uuid import UUID, uuid4
from commons.task import Task
from commons.queue_controller import requestFromQueue
import jsonpickle
import os
from pathlib import Path
from commons.service_types import Service


class TaskManager:

    def __init__(self, service: Service):
        self.corr_id = str(uuid4())
        self.__taskStatus = dict()
        self.service_type: Service = service
        Path("../persistence").mkdir(exist_ok=True, parents=True)

    def removeTask(self, taskID: UUID, persist=False):
        self.__taskStatus.pop(str(taskID))
        if persist:
            self.__persistTasks()

    def updateTask(self, task: Task, persist=False):
        self.__taskStatus[str(task.taskID)] = task
        if persist:
            self.__persistTasks()

    def getTask(self, taskID: UUID):
        task: Task = self.__taskStatus[str(taskID)]

        return task

    def hasTask(self, taskID: UUID):
        return str(taskID) in self.__taskStatus

    def cancelTask(self, taskID: UUID):
        self.__taskStatus[str(taskID)].setStatus(Task.Status.CANCELLED)

        return self.__taskStatus[str(taskID)]

    def getAllTasks(self):
        return {"tasks": list(task.toJson()
                              for task in self.__taskStatus.values())}

    def getAllTasksPickled(self):
        return jsonpickle.encode(self.__taskStatus)

    def getStateFromNetwork(self, blocking: bool = True,
                            persist: bool = False):

        if self.service_type == Service.PREDICTION:
            response = requestFromQueue(
                "persistent_task_status_p", self.corr_id, blocking)
        elif self.service_type == Service.TRAINING:
            response = requestFromQueue(
                "persistent_task_status_t", self.corr_id, blocking)
        else:
            response = requestFromQueue(
                "erroneous_queue", self.corr_id, blocking)

        if not response:
            return False

        response_decoded = jsonpickle.decode(response)
        self.__taskStatus = response_decoded
        print(
            f"Initialised task status dict from network to: {self.__taskStatus}")

        if persist:
            self.__persistTasks()

        return True

    def getStateFromDisk(self):
        if not os.path.isfile(self.__getPath()):
            print("task_status file not found. Setting task status dict to empty...")
            return

        with open(self.__getPath(), "r") as infile:
            encoded_tasks = infile.read()
            self.__taskStatus = jsonpickle.decode(encoded_tasks)

        print(
            f"Persistent task status dict initialised from disk to: {self.__taskStatus}")

    def __persistTasks(self):
        with open(self.__getPath(), "w+") as outfile:
            outfile.write(jsonpickle.encode(self.__taskStatus))
        print(f"Persisted task status dict state as: {self.__taskStatus}")

    def __getPath(self):
        if self.service_type == Service.PREDICTION:
            return "../persistence/task_status_p"
        elif self.service_type == Service.TRAINING:
            return "../persistence/task_status_t"
