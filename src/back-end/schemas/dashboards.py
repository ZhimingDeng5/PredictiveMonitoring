from pydantic import BaseModel
from typing import List
from fastapi import File, UploadFile

# class RequestFile(BaseModel):
#     monitor: UploadFile = File(...)
#     event_log: UploadFile = File(...)


class CreationRequest(BaseModel):
    # file: RequestFile
    monitor: UploadFile = File(...)
    event_log: UploadFile = File(...)


# class CreationResponse(BaseModel):
#     id: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"