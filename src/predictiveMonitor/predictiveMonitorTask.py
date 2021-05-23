from fastapi.param_functions import File
from apromore.predictiveMonitor.predictor import Predictor
from apromore.ApromoreServiceWapper import predict
#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from apromore.Task import Task
from fastapi import File

class predictMonitorTask(Task):
    predictors=[]
    predict_result: File
 
    def __init__(self, predictors, predict_result, taskID, task_name, time_requested, eventlog, status, time_complete, schema):
        super().__init__(taskID, task_name, time_requested, eventlog, status, time_complete, schema)
        self.predictors = predictors
        self.predict_result = predict_result