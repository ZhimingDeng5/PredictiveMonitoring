#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'

from fastapi import FastAPI
from api.request_handler import request_handler
from services.queue_controller import ThreadedConsumer
from services.task_manager import TaskManager

app = FastAPI(
    title='Predictive Monitor System',
    description='Logic plugin for Apromore\'s Predictive Monitors'
)

app.include_router(request_handler)

# start separate thread for listening to output
@app.on_event("startup")
def startup():
    td = ThreadedConsumer(TaskManager())
    td.start()