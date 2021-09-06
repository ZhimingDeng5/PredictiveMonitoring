from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from uuid import uuid4, UUID
from typing import List
import os
import shutil

from starlette.background import BackgroundTask

from services.cancel_request import CancelRequest
from services.queue_controller import sendTaskToQueue, sendCancelRequest
from services.task import Task
from services.task_manager import TaskManager
from thread_classes.master_consumer_thread import MasterConsumerThread
from schemas.dashboards import CreationResponse
from schemas.tasks import TaskListOut, TaskCancelOut

import services.file_handler as fh


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
    uuid = str(task_uuid)


    #file extension checking
    if not fh.csvCheck(event_log.filename):
        return "Please send Eventlog in .csv format."
    
    if not fh.schemaCheck(schema.filename):
        return "Please send schema in .json format."

    for pfile in predictors:
        if not fh.pickleCheck(pfile.filename):
            return "Please send Pickle in .pkl or .pickle format."

    #save files
    fh.savePredictEventlog(uuid, event_log)
    fh.saveSchema(uuid, schema)
    fh.savePickle(uuid, predictors)


    # build new Task object
    new_task: Task = Task(task_uuid, 
    fh.loadPickle(uuid), 
    fh.loadSchema(uuid, schema.filename), 
    fh.loadPredictEventLog(uuid, event_log.filename))

    # store the task status in task manager
    tasks.updateTask(new_task)

    # send task to rabbitMQ
    sendTaskToQueue(new_task, "persistent_task_status")
    sendTaskToQueue(new_task, "input")

    # on success return the task_id
    return {"task_id": uuid}


@request_handler.post(
    "/cancel/{taskID}", response_model=TaskCancelOut)
def cancel_task(taskID: str):

    taskUUID = UUID(taskID)

    if tasks.hasTask(taskUUID):
        t = tasks.getTask(taskUUID)

        # if cancelling a completed task master needs to delete its files
        if t.status == Task.Status.COMPLETED.name:
            fh.removeTaskFile(taskID)
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
        return FileResponse(fh.loadResult(taskID),
            background=BackgroundTask(fh.removeTaskFile, uuid = taskID)
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
