#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from predictive_monitor.predictive_monitor_task import PredictMonitorTask
from fastapi import File
from predictive_monitor.predictor import Predictor


def createPickle(p: Predictor):
    return File()

def createCSV(t: PredictMonitorTask):
    return File()

def createParquet(t: PredictMonitorTask):
    return File()

def convertParquet2Csv(parquet: File):
    return File()

def convertCsv2Parquet(csv: File):
    return File()

