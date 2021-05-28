#!/usr/bin/python3
# -*- encoding: utf-8 -*-

from fastapi import File

def validatelog(eventlog: File, schema: File):
    return File()