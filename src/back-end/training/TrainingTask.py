#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from predictiveMonitor.predictor import Predictor
from Task import Task
from fastapi import File

class predictMonitorTask(Task):
    predictor: Predictor
    filter: File
 
    def __init__(self, predictor, filter, taskID, task_name, time_requested, eventlog, status, time_complete, schema):
        super().__init__(taskID, task_name, time_requested, eventlog, status, time_complete, schema)
        self.predictor = predictor
        self.filter = filter