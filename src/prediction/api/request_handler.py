from fastapi import APIRouter, status, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from uuid import uuid4, UUID
from typing import List

from socket import gaierror
from pika import exceptions

from starlette.background import BackgroundTask

from commons.service_types import Service
from commons.cancel_request import CancelRequest
from commons.queue_controller import sendTaskToQueue, sendCancelRequest
from commons.task_manager import TaskManager
from commons.task import Task
from commons.thread_classes.master_consumer_thread import MasterConsumerThread
from schemas.dashboards import CreationResponse
from schemas.tasks import TaskListOut, TaskCancelOut

import commons.file_handler as fh
import os
import services.validator as vd

request_handler: APIRouter = APIRouter()
tasks: TaskManager = TaskManager(Service.PREDICTION)
master_corr_id: str = str(uuid4())
td: MasterConsumerThread


@request_handler.post(
    "/create-dashboard", status_code=201, response_model=CreationResponse)
def create_dashboard(predictors: List[UploadFile] = File(...),
                     schema: UploadFile = File(...),
                     event_log: UploadFile = File(...)):

    # assign new UUID
    task_uuid: UUID = uuid4()
    uuid: str = str(task_uuid)
    parquet_log: bool = False

    # file extension checking
    if not fh.csvCheck(event_log.filename):
        if fh.parquetCheck(event_log.filename):
            parquet_log = True
        else:    
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Received event log was not in .csv/.parquet format.")

    if not fh.schemaCheck(schema.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received schema was not in .json format."
        )

    for pfile in predictors:
        if not fh.pickleCheck(pfile.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One of the received predictors was not in .pkl or .pickle format."
            )

    # save files
    print("Saving files...")
    fh.savePredictEventlog(uuid, event_log)
    fh.savePredictSchema(uuid, schema)
    fh.savePredictor(uuid, predictors)

    print(f'Task {uuid} files saved...')

    log_address: str = fh.loadPredictEventLogAddress(uuid, event_log.filename)

    # convert parquet file to csv
    if parquet_log:
        log_address = fh.parquetGenerateCsv(uuid, event_log.filename, log_address)

    # file validation
    print("start validating event log file...")
    res = vd.validate_csv_in_path(
        fh.loadPredictEventLogAddress(uuid, event_log.filename),
        fh.loadPredictSchemaAddress(uuid, schema.filename))
    if not res['isSuccess']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fail to validate event log: " + event_log.filename + "[" + res['msg'] + "]")
    print("event log file is correct")

    for pfile in predictors:
        pfile_path = os.path.join(fh.loadPredictorAddress(uuid), pfile.filename)
        print("start validating " + pfile.filename + "...")
        res = vd.validate_pickle_in_path(pfile_path)
        if not res['isSuccess']:
            fh.removePredictTaskFile(uuid)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="fail to validate predictor: " + pfile.filename + " [" + res['msg'] + "]")
        print(pfile.filename + " file is correct")

    print(f'Task {uuid} validation passed...')

    # build new Task object
    new_task: Task = Task(task_uuid,
                          predictors_path=fh.loadPredictorAddress(uuid),
                          config_path="",
                          schema_path=fh.loadPredictSchemaAddress(uuid, schema.filename),
                          event_log_path=log_address)

    # store the task status in task manager
    tasks.updateTask(new_task)

    # send task to rabbitMQ
    try:
        sendTaskToQueue(new_task, "persistent_task_status_p")
        sendTaskToQueue(new_task, "input_p")
    except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
        print("Server was unable to send a message to RabbitMQ in response to dashboard creation request...")
        tasks.removeTask(task_uuid)
        fh.removePredictTaskFile(uuid)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server unable to communicate with RabbitMQ, please try again later."
        )
    
    # on success return the task_id
    return {"task_id": uuid}


@request_handler.post(
    "/cancel/{taskID}", response_model=TaskCancelOut)
def cancel_task(taskID: str):

    taskUUID: UUID = UUID(taskID)

    if tasks.hasTask(taskUUID):
        t = tasks.getTask(taskUUID)

        # if cancelling a completed task master needs to delete its files
        if t.status == Task.Status.COMPLETED.name:
            print(f"Received a request to cancel completed task {taskID}...")
            try:
                t.setStatus(Task.Status.CANCELLED)
                # remove the task from the persistence node
                sendTaskToQueue(t, "persistent_task_status_p")
                print(f"Deleting result files corresponding to task {taskID} in response to a cancel request...")
                fh.removePredictTaskFile(taskID)
            except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
                t.setStatus(Task.Status.COMPLETED)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Server unable to communicate with RabbitMQ, please try again later."
                )
        # if cancelling an error state task remove it from master & persistence
        # (task files were already removed by worker)
        elif t.status == Task.Status.ERROR.name:
            print(f"Received a request to cancel error state task {taskID}...")
            try:
                t.setStatus(Task.Status.CANCELLED)
                sendTaskToQueue(t, "persistent_task_status_p")

                print(f"Cancel request for {taskID} processed.")
            except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
                t.setStatus(Task.Status.ERROR)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Server unable to communicate with RabbitMQ, please try again later."
                )

        # if cancelling an incomplete task we let the worker know. It'll delete the task files
        else:
            try:
                sendCancelRequest(CancelRequest(taskUUID), master_corr_id, Service.PREDICTION)
            except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
                print("Server was unable to send a message to RabbitMQ in response to dashboard cancel request...")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Server unable to communicate with RabbitMQ, please try again later."
                )

        # remove the task from master node's task manager
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

        if tasks.getTask(taskUUID).status != Task.Status.COMPLETED.name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Task with id {taskID} is not yet completed."
            )

        # cancelled tasks are not persisted, so sending a cancelled task will delete it from the persistence node
        try:
            tasks.cancelTask(taskUUID)
            sendTaskToQueue(tasks.getTask(taskUUID), "persistent_task_status_p")
        except (gaierror, exceptions.ConnectionClosed, exceptions.ChannelClosed, exceptions.AMQPError) as err:
            tasks.getTask(taskUUID).setStatus(Task.Status.COMPLETED)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server unable to communicate with RabbitMQ, please try again later."
            )
        tasks.removeTask(taskUUID)

        print(f"Responding to a file request for task {taskID}...")
        return FileResponse(fh.loadPredictResult(taskID),
                            background=BackgroundTask(fh.removePredictTaskFile, uuid=taskID))

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id: {taskID} not found.",
        )


@request_handler.on_event("startup")
def startup():
    tasks.getStateFromNetwork()
    global td
    td = MasterConsumerThread(tasks, Service.PREDICTION)
    td.start()
