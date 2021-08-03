from uuid import UUID
from enum import Enum
import json


class Task:
    class Status(Enum):
        QUEUED = 0
        PROCESSING = 1
        COMPLETED = 2

    def __init__(self, id: UUID, filepath: str, status: Status = Status.QUEUED):
        self.id = str(id)
        self.filepath = filepath
        self.status = status.name

    def setStatus(self, status: Status):
        self.status = status.name

    def toJsonS(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toJson(self):
        return {"id": self.id, "filepath": self.filepath, "status": self.status}

    @staticmethod
    def fromJsonS(jsonString: str):
        obj = json.loads(jsonString)
        return Task(obj["id"], obj["filepath"], Task.Status[obj["status"]])
