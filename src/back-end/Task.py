#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from datetime import datetime
from fastapi import File
from pydantic import BaseModel


class Task(object):
    task_ID: int
    task_name: str
    time_requested: datetime
    eventlog: File
    status: str
    time_complete: datetime
    schema: File

    def __init__(self, task_ID, task_name, time_requested, eventlog, status, time_complete, schema):
        self.task_ID = task_ID
        self.task_name = task_name
        self.time_requested = time_requested
        self.eventlog = eventlog
        self.status = status
        self.time_complete = time_complete
        self.schema = schema




