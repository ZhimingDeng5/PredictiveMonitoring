#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'

from fastapi import APIRouter, UploadFile, File
from typing import Optional, List
from rabbitmq import master_queue_controller as mq
import apromore_service_wapper as apro_service
from Task import Task
from datetime import datetime

test = APIRouter()


# put interfaces here

@test.get('/')
async def default():
    mq.pushTask(Task(1,"1",datetime.today(),None,"0",datetime.today(),None))
    return {'message': 'done'}


