from uuid import UUID
from services.task import Task


class TaskManager:

    __taskStatus = dict()

    def removeTask(self, taskID: UUID):
        self.__taskStatus.pop(str(taskID))

    def updateTask(self, task: Task):
        self.__taskStatus[str(task.taskID)] = task

    def getTask(self, taskID: UUID):
        task: Task = self.__taskStatus[str(taskID)]

        if task.status == Task.Status.COMPLETED.name or task.status == Task.Status.CANCELLED.name:
            self.__taskStatus.pop(task.taskID)

        return task

    def hasTask(self, taskID: UUID):
        return str(taskID) in self.__taskStatus

    def getAllTasks(self):
        print({"tasks": list(task.toJson() for task in self.__taskStatus.values())})
        return {"tasks": list(task.toJson() for task in self.__taskStatus.values())}
