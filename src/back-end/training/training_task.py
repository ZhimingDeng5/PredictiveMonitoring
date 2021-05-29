#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from predictive_monitor.predictor import Predictor
from Task import Task
from fastapi import File

class TrainingTask(Task):
    predictor: Predictor
    filter: File
 
    def __init__(self, predictor, filter, task_ID, task_name, time_requested, eventlog, status, time_complete, schema):
        super().__init__(task_ID, task_name, time_requested, eventlog, status, time_complete, schema)
        self.predictor = predictor
        self.filter = filter