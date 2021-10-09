from pydantic import BaseModel


# class CreationRequest(BaseModel):
#     predictors: List[UploadFile] = File(...)
#     schema: UploadFile = File(...)
#     event_log: UploadFile = File(...)


class CreationResponse(BaseModel):
    task_id: str = "45a2c5f3-1f67-495e-a2af-dc20117f232d"
