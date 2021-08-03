from pydantic import BaseModel
from typing import List

class TaskOut(BaseModel):
    id: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"
    name: str = "Default Task"
    status: str = "QUEUED"


class TaskListOut(BaseModel):
    tasks: List[TaskOut]
