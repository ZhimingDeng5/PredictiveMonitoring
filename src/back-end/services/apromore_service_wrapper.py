#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'

from predictive_monitor.predictive_monitor_task import PredictMonitorTask
from training.training_task import TrainingTask


def predict(t: PredictMonitorTask):
    return PredictMonitorTask()


def training(t: TrainingTask):
    return TrainingTask()
