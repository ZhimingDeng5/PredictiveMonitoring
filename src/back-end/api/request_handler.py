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
from thread_classes.master_consumer_thread import MasterConsumerThread
from schemas.dashboards import CreationResponse
from schemas.tasks import TaskListOut, TaskCancelOut
from starlette.background import BackgroundTask

request_handler = APIRouter()
tasks = TaskManager()
master_corr_id = str(uuid4())


@request_handler.post(
    "/create-dashboard", status_code=201, response_model=CreationResponse)
def create_dashboard(predictors: List[UploadFile] = File(...),
                     schema: UploadFile = File(...),
                     event_log: UploadFile = File(...)):

    # assign new UUID
    task_uuid = uuid4()

    # generate path to save the received files at
    predictors_path = os.path.join("task_files", f"{str(task_uuid)}-predictors")
    schema_path = os.path.join("task_files", f"{str(task_uuid)}-schema")
    event_log_path = os.path.join("task_files", f"{str(task_uuid)}-event_log")

    # extract the data from the request
    schema_object = schema.file
    event_log_object = event_log.file

    os.mkdir(predictors_path)

    # save the files
    for predictor in predictors:
        predictor_object = predictor.file
        predictor_path: str = f"{predictors_path}/{predictor.filename}"
        with open(predictor_path, "wb") as outfile:
            shutil.copyfileobj(predictor_object, outfile)
    with open(schema_path, "wb") as outfile:
        shutil.copyfileobj(schema_object, outfile)
    with open(event_log_path, "wb") as outfile:
        shutil.copyfileobj(event_log_object, outfile)

    # build new Task object
    new_task: Task = Task(task_uuid, predictors_path, schema_path, event_log_path)

    # store the task status in task manager
    tasks.updateTask(new_task)

    # send task to rabbitMQ
    sendTaskToQueue(new_task, "persistent_task_status")
    sendTaskToQueue(new_task, "input")

    # on success return the task_id
    return {"task_id": str(task_uuid)}


@request_handler.delete(
    "/cancel/{taskID}", response_model=TaskCancelOut)
def cancel_task(taskID: str):

    taskUUID = UUID(taskID)

    if tasks.hasTask(taskUUID):
        t = tasks.getTask(taskUUID)

        # if cancelling a completed task master needs to delete its files
        if t.status == Task.Status.COMPLETED.name:
            os.remove(os.path.join("task_files", f"{taskUUID}-results.csv"))
            print(f"Deleting result files corresponding to task {taskID} in response to a cancel request...")

        # if cancelling an incomplete task we let the worker know. It'll delete the task files
        else:
            sendCancelRequest(CancelRequest(taskUUID), master_corr_id)

        # remove the task from the persistence node
        t.setStatus(Task.Status.CANCELLED)
        sendTaskToQueue(t, "persistent_task_status")

        # remove the task from master node
        tasks.removeTask(taskUUID)

        print(f"Removed task {taskID} from the task manager in response to a cancel request...")
        return t.toJson()
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

        # cancelled tasks are not persisted, so sending a cancelled task will delete it from the persistence node
        tasks.cancelTask(taskUUID)
        sendTaskToQueue(tasks.getTask(taskUUID), "persistent_task_status")
        tasks.removeTask(taskUUID)

        print(f"Responding to a file request for task {taskID}...")

        return FileResponse(
            os.path.join("task_files", f"{taskID}-results.csv"),
            background=BackgroundTask(__remove_task_files, taskID)
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {taskID} not found.",
        )


def __remove_task_files(taskUUID: str):
    os.remove(os.path.join("task_files", f"{taskUUID}-results.csv"))
    print(f"Removed task {taskUUID} from the task manager...")


@request_handler.on_event("startup")
def startup():
    tasks.getStateFromNetwork()
    td = MasterConsumerThread(tasks)
    td.start()
