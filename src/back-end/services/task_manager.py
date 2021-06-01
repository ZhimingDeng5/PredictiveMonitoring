from uuid import UUID
from services.task import Task


class TaskManager:

    __taskStatus = dict()

    def removeTask(self, id: UUID):
        self.__taskStatus.pop(str(id))

    def updateTask(self, task: Task):
        self.__taskStatus[str(task.id)] = task

    def getTask(self, id: UUID):
        task: Task = self.__taskStatus[str(id)]

        if task.status == Task.Status.COMPLETED.name:
            self.__taskStatus.pop(task.id)

        return task

    def hasTask(self, id: UUID):
        return str(id) in self.__taskStatus

    def getAllTasks(self):
        return {"tasks": list(task.toJson() for task in self.__taskStatus.values())}
