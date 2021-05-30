#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'

from fastapi import APIRouter, UploadFile, File
from typing import Optional, List
from predictive_monitor.task_handler import store_and_send, get_tasks_by_id

predictive_monitor = APIRouter()


# put interfaces here

@predictive_monitor.get('/')
async def default():
    return {'message': 'This is predictive monitor module'}


@predictive_monitor.post('/create-monitor')
async def create_monitor(monitor_name: str, eventlog: UploadFile = File(...)):
    contents = await eventlog.read()
    task_uuid = store_and_send({'monitor_name': monitor_name, "eventlog": contents})
    return {"uuid": task_uuid}


@predictive_monitor.get('/poll/{task_id}')
async def poll(task_id: str):
    tasks = task_id.split('&')
    return get_tasks_by_id(tasks)
