import jsonpickle
import os
import pytest
from uuid import UUID, uuid4

from services.task import Task
from services.task_manager import TaskManager


@pytest.fixture
def empty_tm():
    empty_tm = TaskManager()
    return empty_tm

@pytest.fixture
def task_uuid():
    task_uuid = uuid4()
    return task_uuid

@pytest.fixture
def task_status(task_uuid):
    task_id = str(task_uuid)
    task_status = jsonpickle.encode({task_id: Task(task_id, "", "", "", Task.Status.QUEUED)})
    return task_status

@pytest.fixture
def tm(empty_tm, task_status, mocker):
    m = mocker.patch('builtins.open', mocker.mock_open(read_data = task_status))
    empty_tm.getStateFromDisk()
    return empty_tm

# Tests the proper initialisation of the CancellationHandler
def test_init(empty_tm):
    assert empty_tm.getAllTasks() == {"tasks": []}

# Tests updating own task status from disk
def test_update_from_disk(empty_tm, task_uuid, task_status, mocker):
    m = mocker.patch('builtins.open', mocker.mock_open(read_data = task_status))
    empty_tm.getStateFromDisk()

    m.assert_called_once_with("../persistence/task_status", "r")
    assert empty_tm.hasTask(task_uuid)

# Tests updating own task status from network
def test_update_from_network(empty_tm, task_uuid, task_status, mocker):
    m = mocker.patch('services.task_manager.requestFromQueue', return_value = task_status)
    empty_tm.getStateFromNetwork()
    assert empty_tm.hasTask(task_uuid)

# Tests the removal of tasks
def test_remove_task(tm, task_uuid):
    tm.removeTask(task_uuid)
    assert not tm.hasTask(task_uuid)
    assert tm.getAllTasks() == {"tasks": []}

# Tests the update of tasks
def test_update_task(tm, task_uuid):
    t1 = tm.getTask(task_uuid)
    t2 = Task(task_uuid, "", "", "", Task.Status.PROCESSING)
    tm.updateTask(t2)
    t3 = tm.getTask(task_uuid)
    assert t1 != t3

# Tests the cancellation of tasks
def test_cancel_task(tm, task_uuid):
    tm.cancelTask(task_uuid)
    assert tm.getTask(task_uuid).status == Task.Status.CANCELLED.name