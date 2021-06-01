from fastapi import APIRouter, Response, status, HTTPException
from uuid import UUID, uuid4
import json
from services.queue_controller import ThreadedConsumer, sendTaskToQueue
from services.task import Task
from services.task_manager import TaskManager
from schemas.dashboards import RequestFile, CreationRequest, CreationResponse
from schemas.tasks import TaskOut, TaskListOut

request_handler = APIRouter()
tasks = TaskManager()


@request_handler.post(
    "/create-dashboard", status_code=201
)  # , response_model=schemas.CreationResponse)
def create_dashboard(request: CreationRequest):

    # # assign new UUID
    task_uuid = uuid4()

    # # generate path to save the received file at
    path: str = f"task_files/{str(task_uuid)}.json"

    # # extract the data form the request
    data = request.file.dict()

    # # save the file
    with open(path, "w") as outfile:
        json.dump(data, outfile)

    # # build new Task object
    new_task: Task = Task(task_uuid, path)

    # # store the task status in task manager
    tasks.updateTask(new_task)

    # # send task to rabbitMQ
    sendTaskToQueue(new_task, "input")

    # # on success return the task_id
    return {"task_id": str(task_uuid)}


@request_handler.get("/tasks", response_model=TaskListOut)
def get_all_tasks():
    return tasks.getAllTasks()


@request_handler.get("/task/{id}", response_model=TaskListOut)
def get_task(id: str):
    id_list = id.split("&")
    response = []
    for id in id_list:
        if tasks.hasTask(id):
            response.append(tasks.getTask(id).toJson())
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id: {id} not found.",
            )
    return {"tasks": response}