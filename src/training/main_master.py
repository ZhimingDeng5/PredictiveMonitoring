#!/usr/bin/python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.request_handler import request_handler

app = FastAPI(
    openapi_prefix="/training",
    title="Predictive Monitor System",
    description="Logic plugin for Apromore's Predictive Monitors"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(request_handler)


if __name__ == '__main__':
    uvicorn.run('main_master:app', host='0.0.0.0', port=8000, workers=1)
