#!/usr/bin/python3
# -*- encoding: utf-8 -*-


from fastapi import File


def filt_File(eventlog: File, type: str):
    return File()