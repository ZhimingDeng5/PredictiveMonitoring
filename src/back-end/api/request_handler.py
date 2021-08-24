from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from uuid import uuid4, UUID
from typing import List
import os
import shutil

from services.cancel_request import CancelRequest
from services.queue_controller import sendTaskToQueue, sendCancelRequest
from services.task import Task
from services.task_manager import TaskManager
from schemas.dashboards import CreationResponse
from schemas.tasks import TaskListOut, TaskCancelOut

request_handler = APIRouter()
tasks = TaskManager()
master_corr_id = str(uuid4())


@request_handler.post(
    "/create-dashboard", status_code=201, response_model=CreationResponse)
def create_dashboard(monitor: List[UploadFile] = File(...), event_log: UploadFile = File(...)):

    # assign new UUID
    task_uuid = uuid4()

    # generate path to save the received files at
    monitor_path: str = f"task_files/{str(task_uuid)}-monitor"
    event_log_path: str = f"task_files/{str(task_uuid)}-event_log"


    # extract the data from the request
    event_log_object = event_log.file
    # monitor_object = monitor.file

    os.mkdir(monitor_path)


    # save the files
    for predictor in monitor:
        predictor_object = predictor.file
        predictor_path: str = f"{monitor_path}/{predictor.filename}"
        with open(predictor_path, "wb") as outfile:
            shutil.copyfileobj(predictor_object, outfile)
    with open(event_log_path, "wb") as outfile:
        shutil.copyfileobj(event_log_object, outfile)

    # build new Task object
    new_task: Task = Task(task_uuid, monitor_path, event_log_path)

    # store the task status in task manager
    tasks.updateTask(new_task)

    # send task to rabbitMQ
    sendTaskToQueue(new_task, "input")

    # on success return the task_id
    return {"task_id": str(task_uuid)}


@request_handler.delete(
    "/cancel/{taskID}", response_model=TaskCancelOut)
def cancel_task(taskID: str):

    taskUUID = UUID(taskID)

    if tasks.hasTask(taskUUID):
        tasks.cancelTask(taskUUID)
        sendCancelRequest(CancelRequest(taskUUID), master_corr_id)
        print(f"Set status of task {taskID} to: {Task.Status.CANCELLED.name}")
        return tasks.getTask(taskUUID).toJson()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {taskID} not found."
        )


@request_handler.get("/tasks", response_model=TaskListOut)
def get_all_tasks():
    return tasks.getAllTasks()


@request_handler.get("/task/{taskIDs}", response_model=TaskListOut)
def get_task(taskIDs: str):
    id_list = taskIDs.split("&")
    response = []
    for id_string in id_list:
        taskID = UUID(id_string)
        if tasks.hasTask(taskID):
            response.append(tasks.getTask(taskID).toJson())
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id: {taskID} not found.",
            )
    return {"tasks": response}


@request_handler.get("/dashboard/{taskID}")
def download_result(taskID: str):
    taskUUID = UUID(taskID)
    if tasks.hasTask(taskUUID):
        tasks.removeTask(taskUUID)
        return FileResponse(f"task_files\\{taskID}-results.csv")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {taskID} not found.",
        )
