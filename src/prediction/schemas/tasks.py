from fastapi import File, UploadFile
from pydantic import BaseModel
from typing import List


class TaskOut(BaseModel):
    taskID: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"
    status: str = "QUEUED"


class TaskListOut(BaseModel):
    tasks: List[TaskOut]


class TaskCancelOut(BaseModel):
    taskID: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"
    status: str = "CANCELLED"
