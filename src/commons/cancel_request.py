from uuid import UUID
import json


class CancelRequest:

    def __init__(self, taskID: UUID, cancelled: bool = False):
        self.taskID: str = str(taskID)
        self.cancelled: bool = cancelled

    def toJsonS(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def fromJsonS(jsonString: str):
        obj = json.loads(jsonString)
        return CancelRequest(obj["taskID"], obj["cancelled"])
