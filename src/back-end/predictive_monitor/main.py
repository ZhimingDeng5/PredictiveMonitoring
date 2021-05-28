#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'

from fastapi import APIRouter, UploadFile, File
from typing import Optional, List

predictive_monitor = APIRouter()


# put interfaces here

@predictive_monitor.get('/')
async def default():
    return {'message': 'This is predictive monitor module'}


@predictive_monitor.post('/create_monitor')
async def create_monitor(monitor_name: str, pickle_files: List[UploadFile] = File(...),
                         schema_file: UploadFile = File(...)):
    pass
    # validation and creation

    return {'monitor_name': monitor_name, 'pickle_files': [file.filename for file in pickle_files],
            'schema_file': schema_file.filename}
