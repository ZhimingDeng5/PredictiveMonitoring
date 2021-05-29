#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# __author__ = '__Leo__'

import uvicorn, time
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from training import training
from predictive_monitor import predictive_monitor

app = FastAPI(
    title='Apromore Project',
    description='Business Processing',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# mount static resources in directory '/static'
app.mount(path='/static', app=StaticFiles(directory='./static'),
          name="static")

# @prefix: prefix path
app.include_router(predictive_monitor, prefix='/predictive_monitor', tags=['Predictive Monitor Module'])
app.include_router(training, prefix='/training', tags=['Training Module'])


if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)

