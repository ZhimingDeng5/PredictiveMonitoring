from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from uuid import uuid4, UUID
from typing import List
import os

from starlette.background import BackgroundTask

from services.cancel_request import CancelRequest
from services.queue_controller import sendTaskToQueue, sendCancelRequest
from services.task import Task
from services.task_manager import TaskManager
from thread_classes.master_consumer_thread import MasterConsumerThread
from schemas.dashboards import CreationResponse
from schemas.tasks import TaskListOut, TaskCancelOut

import services.file_handler as fh
import services.validator as vd

request_handler = APIRouter()
tasks = TaskManager()
master_corr_id = str(uuid4())
td: MasterConsumerThread

@request_handler.post(
    "/create-dashboard", status_code=201, response_model=CreationResponse)
def create_dashboard(predictors: List[UploadFile] = File(...),
                     schema: UploadFile = File(...),
                     event_log: UploadFile = File(...)):

    # assign new UUID
    task_uuid = uuid4()
    uuid = str(task_uuid)
    parquet_log = False

    # file extension checking
    if not fh.csvCheck(event_log.filename):
        if fh.parquetCheck(event_log.filename):
            parquet_log = True
        else:    
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Please send Eventlog in .csv/.parquet format.")
    
    if not fh.schemaCheck(schema.filename):
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Please send schema in .json format.")

    for pfile in predictors:
        if not fh.pickleCheck(pfile.filename):
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail="Please send Pickle in .pkl or .pickle format.")

    # save files
    fh.savePredictEventlog(uuid, event_log)
    fh.savePredictSchema(uuid, schema)
    fh.savePredictor(uuid, predictors)

    log_address = fh.loadPredictEventLogAddress(uuid, event_log.filename)

    # convert parquet file to csv
    if parquet_log:
        filename, extension = os.path.splitext(event_log.filename)
        new_log = fh.loadPredictEventLogAddress(uuid,filename) + '.csv'
        fh.parquet2Csv(log_address, new_log)
        fh.removeFile(log_address)
        log_address = new_log

    res = vd.validate_csv_in_path(
        log_address,
        fh.loadPredictSchemaAddress(uuid, schema.filename))
    if not res['isSuccess']:
        fh.removePredictTaskFile(uuid)
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=res['msg'])

    for pfile in predictors:
        res = vd.validate_pickle_in_path(fh.loadPredictorAddress(uuid)+"\\"+pfile.filename)
        if not res['isSuccess']:
            fh.removePredictTaskFile(uuid)
            raise HTTPException(
                status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
                detail=res['msg'])

    # build new Task object
    new_task: Task = Task(task_uuid,
                          fh.loadPredictorAddress(uuid),
                          fh.loadPredictSchemaAddress(uuid, schema.filename),
                          log_address)

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
            fh.removePredictTaskFile(taskID)
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


# todo: make it so that it returns partial results
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

        # TODO: add check for whether the task is completed

        # cancelled tasks are not persisted, so sending a cancelled task will delete it from the persistence node
        tasks.cancelTask(taskUUID)
        sendTaskToQueue(tasks.getTask(taskUUID), "persistent_task_status")
        tasks.removeTask(taskUUID)

        print(f"Responding to a file request for task {taskID}...")
        return FileResponse(fh.loadPredictResult(taskID),
                            background=BackgroundTask(fh.removePredictTaskFile, uuid=taskID))

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
    global td
    td = MasterConsumerThread(tasks)
    td.start()
