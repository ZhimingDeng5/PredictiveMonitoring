from uuid import UUID
from enum import Enum
import json


class Task:
    class Status(Enum):
        QUEUED = 0
        PROCESSING = 1
        COMPLETED = 2
        CANCELLED = 3

    def __init__(self, taskID: UUID,
                 # TRAINING/PREDICTION SPLIT
                 predictors_path: str,
                 config_path: str,
                 schema_path: str,
                 event_log_path: str,
                 status: Status = Status.QUEUED):
        self.taskID = str(taskID)
        # TRAINING/PREDICTION SPLIT
        self.predictors_path = predictors_path
        self.config_path = config_path
        self.schema_path = schema_path
        self.event_log_path = event_log_path
        self.status: Task.Status = status.name

    def __eq__(self, other):
        return self.taskID == other.taskID and \
               # TRAINING/PREDICTION SPLIT
               self.predictors_path == other.predictors_path and \
               self.config_path == other.config_path and \
               self.schema_path == other.schema_path and \
               self.event_log_path == other.event_log_path and \
               self.status == other.status

    def setStatus(self, status: Status):
        self.status = status.name

    def toJsonS(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toJson(self):
        return {"taskID": self.taskID,
                # TRAINING/PREDICTION SPLIT
                "predictors_path": self.predictors_path,
                "config_path": self.config_path,
                "schema_path": self.schema_path,
                "event_log_path": self.event_log_path,
                "status": self.status}

    def __repr__(self):
        return self.toJsonS()

    @staticmethod
    def fromJsonS(jsonString: str):
        obj = json.loads(jsonString)
        # TRAINING/PREDICTION SPLIT
        return Task(obj["taskID"], obj["predictors_path"], obj["config_path"], obj["schema_path"], obj["event_log_path"], Task.Status[obj["status"]])
