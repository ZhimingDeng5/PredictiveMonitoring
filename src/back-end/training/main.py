#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'
from fastapi import APIRouter, Form, File, UploadFile
from enum import Enum
from training import schemas

training = APIRouter()


# put interfaces here

class PredictorType(str, Enum):
    binary = 'binary'
    remaining_time = 'remaining time'


@training.get('/')
def default():
    return {'message': 'This is training module'}


@training.post('/generate_predictor')
def generate_predictor(predictor_type: PredictorType, predictor_name: str, event_log_file: UploadFile = File(...),
                       schema_file: UploadFile = File(...)):
    # validation and generating the predictor
    pass
    message = {"predictor_type": predictor_type, 'predictor_name': predictor_name,
               'event_log_file': event_log_file.filename, 'schema_file': schema_file.filename}
    return message
