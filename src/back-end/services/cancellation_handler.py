from uuid import UUID


class CancellationHandler:
    __current_task: UUID = UUID("00000000-0000-0000-0000-000000000000")
    __cancelSet = set()

    def getCurrentTask(self):
        return self.__current_task

    def setCurrentTask(self, taskID: UUID):
        self.__current_task = taskID

    def addCancel(self, taskID: UUID):
        self.__cancelSet.add(taskID)

    def hasCancel(self, taskID: UUID):
        return taskID in self.__cancelSet

    def removeCancel(self, taskID: UUID):
        self.__cancelSet.discard(taskID)

    def getAllCancel(self):
        return {f"UUIDs in cancel set": {self.__cancelSet}}
