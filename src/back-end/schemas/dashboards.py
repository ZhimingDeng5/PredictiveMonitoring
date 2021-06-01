from pydantic import BaseModel
from typing import List

class RequestFile(BaseModel):
    monitor: str
    events: List[str]


class CreationRequest(BaseModel):
    file: RequestFile


class CreationResponse(BaseModel):
    id: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"