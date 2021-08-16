from uuid import UUID
from enum import Enum
import json


class Task:
    class Status(Enum):
        QUEUED = 0
        PROCESSING = 1
        COMPLETED = 2
        DOWNLOADED = 3
        CANCELLED = 4

    def __init__(self, taskID: UUID, monitor_path: str, event_log_path: str, status: Status = Status.QUEUED):
        self.taskID = str(taskID)
        self.monitor_path = monitor_path
        self.event_log_path = event_log_path
        self.status = status.name

    def setStatus(self, status: Status):
        self.status = status.name

    def toJsonS(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toJson(self):
        return {"taskID": self.taskID,
                "monitor_path": self.monitor_path,
                "event_log_path": self.event_log_path,
                "status": self.status}

    @staticmethod
    def fromJsonS(jsonString: str):
        obj = json.loads(jsonString)
        return Task(obj["taskID"], obj["monitor_path"], obj["event_log_path"], Task.Status[obj["status"]])
