from uuid import UUID, uuid4
from commons.task import Task
from src.commons.queue_controller import requestFromQueue
import jsonpickle
import os
from pathlib import Path


class TaskManager:

    def __init__(self, persistence_queue_name: str):
        self.corr_id = str(uuid4())
        self.__taskStatus = dict()
        self.persistence_queue_name: str = persistence_queue_name
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
        return {"tasks": list(task.toJson() for task in self.__taskStatus.values())}

    def getAllTasksPickled(self):
        return jsonpickle.encode(self.__taskStatus)

    def getStateFromNetwork(self, blocking: bool = True, persist: bool = False):

        response = requestFromQueue(self.persistence_queue_name, self.corr_id, blocking)

        if not response:
            return False

        response_decoded = jsonpickle.decode(response)
        self.__taskStatus = response_decoded
        print(f"Initialised task status dict from network to: {self.__taskStatus}")

        if persist:
            self.__persistTasks()

        return True

    def getStateFromDisk(self):
        if not os.path.isfile("../persistence/task_status"):
            print("task_status file not found. Setting task status dict to empty...")
            return

        with open("../persistence/task_status", "r") as infile:
            encoded_tasks = infile.read()
            self.__taskStatus = jsonpickle.decode(encoded_tasks)

        print(f"Persistent task status dict initialised from disk to: {self.__taskStatus}")

    def __persistTasks(self):
        with open("../persistence/task_status", "w+") as outfile:
            outfile.write(jsonpickle.encode(self.__taskStatus))
        print(f"Persisted task status dict state as: {self.__taskStatus}")
