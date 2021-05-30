from fastapi import FastAPI, Response, status, HTTPException
from uuid import UUID, uuid4
from task_manager import TaskManager
import schemas
from task import Task
from queue_controller import ThreadedConsumer, sendTaskToQueue
import json

app = FastAPI()
tasks = TaskManager()


@app.post(
    "/create-dashboard", status_code=201
)  # , response_model=schemas.CreationResponse)
def create_dashboard(request: schemas.CreationRequest):

    # # assign new UUID
    task_uuid = uuid4()

    # # generate path to save the received file at
    path: str = f"taskfiles/{str(task_uuid)}.json"

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


@app.get("/tasks", response_model=schemas.TaskListOut)
def get_all_tasks():
    return tasks.getAllTasks()


@app.get("/task/{id}", response_model=schemas.TaskOut)
def get_task(id: UUID):
    if tasks.hasTask(id):
        return tasks.getTask(id).toJson()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {id} not found.",
        )


# start separate thread for listening to output
@app.on_event("startup")
def startup():
    td = ThreadedConsumer(tasks)
    td.start()

