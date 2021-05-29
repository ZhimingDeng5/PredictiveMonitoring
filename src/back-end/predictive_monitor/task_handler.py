#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# __author__ = '__Jiahao__'
import uuid, json, os

# store UUID : Status
dict = {}


def store_and_send(obj):
    # create task uuid
    task_uuid = str(uuid.uuid1())
    # store uuid and status in dict
    dict[task_uuid] = {
        'status': obj.get('status')
    }
    obj['task_ID'] = task_uuid
    # store locally
    with open(os.path.abspath('..') + '\\back-end\\json_files\\' + task_uuid + '.txt', 'w') as f:
        f.write(json.dumps(obj))
        f.flush()
        f.close()
    # rabbitmq interface
    send_message = {}
    send_message['uuid'] = task_uuid
    send_message['path'] = '..\\json_files\\' + task_uuid
    # pushTask(send_message)
    return task_uuid


def update_status(task_uuid, obj):
    dict[task_uuid]['status'] = obj.get('status')


def get_tasks_by_id(task_IDs):
    # load json files locally
    # return json files
    tasks = {}
    for t in task_IDs:
        f = open(os.path.abspath('..') + '\\back-end\\json_files\\' + t + '.txt', 'r')
        tasks[t] = f.read()
    return tasks
