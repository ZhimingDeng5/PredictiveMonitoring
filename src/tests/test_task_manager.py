import sys
sys.path.insert(1, '../')

import jsonpickle
import os
import pytest
from uuid import uuid4

from commons.task import Task
from commons.task_manager import TaskManager
from commons.service_types import Service

# Task format:
# ts = {"00000000-0000-0000-0000-000000000000": {"py/object": "services.task.Task", "taskID": "00000000-0000-0000-0000-000000000000", "predictors_path": "task_files\\00000000-0000-0000-0000-000000000000-predictors", "schema_path": "task_files\\00000000-0000-0000-0000-000000000000-schema", "event_log_path": "task_files\\00000000-0000-0000-0000-000000000000-event_log", "status": "COMPLETED"}}
# t_id = "00000000-0000-0000-0000-000000000000"
# t_uuid = UUID(t_id)

@pytest.fixture
def t_uuid():
    t_uuid = uuid4()
    return t_uuid

@pytest.fixture
def tm_training():
    tm_training = TaskManager(Service.TRAINING)
    return tm_training

@pytest.fixture
def tm_prediction():
    tm_prediction = TaskManager(Service.PREDICTION)
    return tm_prediction

@pytest.fixture
def ts(t_uuid):
    ts = {str(t_uuid): Task(t_uuid, "", "", "", "", Task.Status.QUEUED)}
    return ts

@pytest.fixture
def tm_training_ts(t_uuid, tm_training, ts):
    tm_training.updateTask(ts[str(t_uuid)])
    tm_training_ts = tm_training
    return tm_training_ts

@pytest.fixture
def tm_prediction_ts(t_uuid, tm_prediction, ts):
    tm_prediction.updateTask(ts[str(t_uuid)])
    tm_prediction_ts = tm_prediction
    return tm_prediction_ts

# @pytest.fixture(autouse = True)
# def maintain_task_status(ts):
#     # Save current task_status before each task
#     with open(os.path.join("..", "persistence", "task_status"), "r") as f_in:
#         old_ts = jsonpickle.decode(f_in.read())
#     with open(os.path.join("..", "persistence", "task_status"), "w") as f_out_test:
#         f_out_test.write(jsonpickle.encode(ts))

#     # Perform test
#     yield
    
#     # Rewrite old task_status after each task
#     with open(os.path.join("..", "persistence", "task_status"), "w") as f_out:
#         f_out.write(jsonpickle.encode(old_ts))


# Tests the proper initialisation of the CancellationHandler
def test_init(tm_training, tm_prediction):
    assert tm_training.getAllTasks() == {"tasks": []}
    assert tm_prediction.getAllTasks() == {"tasks": []}

# Tests updating own task_status from disk
def test_update_from_disk(t_uuid, tm_training, tm_prediction, ts, mocker):
    read_ts = jsonpickle.encode(ts)
    m_check = mocker.patch("os.path.isfile", return_value = True)
    m_read = mocker.patch("builtins.open", mocker.mock_open(read_data = str(read_ts)))
    
    tm_training.getStateFromDisk()
    m_check.assert_called_with("../persistence/task_status_t")
    m_read.assert_called_with("../persistence/task_status_t", "r")
    assert tm_training.hasTask(t_uuid)

    tm_prediction.getStateFromDisk()
    m_check.assert_called_with("../persistence/task_status_p")
    m_read.assert_called_with("../persistence/task_status_p", "r")
    assert tm_prediction.hasTask(t_uuid)

def test_update_from_network(t_uuid, tm_training, tm_prediction, ts, mocker):
    read_ts = jsonpickle.encode(ts)
    m = mocker.patch("commons.task_manager.requestFromQueue", return_value=read_ts)

    tm_training.getStateFromNetwork()
    m.assert_called_with("persistent_task_status_t", tm_training.corr_id, True)
    assert tm_training.hasTask(t_uuid)

    tm_prediction.getStateFromNetwork()
    m.assert_called_with("persistent_task_status_p", tm_prediction.corr_id, True)
    assert tm_prediction.hasTask(t_uuid)


# Tests the removal of tasks
def test_remove_task(t_uuid, tm_training_ts, tm_prediction_ts):
    tm_training_ts.removeTask(t_uuid)
    assert not tm_training_ts.hasTask(t_uuid)
    assert tm_training_ts.getAllTasks() == {"tasks": []}

    tm_prediction_ts.removeTask(t_uuid)
    assert not tm_prediction_ts.hasTask(t_uuid)
    assert tm_prediction_ts.getAllTasks() == {"tasks": []}

# # Tests the update of tasks
def test_update_task(t_uuid, tm_training_ts, tm_prediction_ts):
    t1 = tm_training_ts.getTask(t_uuid)
    t2 = Task(t_uuid, "", "", "", "", Task.Status.PROCESSING)
    tm_training_ts.updateTask(t2)
    t3 = tm_training_ts.getTask(t_uuid)
    assert t1 != t3

    t4 = tm_prediction_ts.getTask(t_uuid)
    t5 = Task(t_uuid, "", "", "", "", Task.Status.PROCESSING)
    tm_prediction_ts.updateTask(t5)
    t6 = tm_prediction_ts.getTask(t_uuid)
    assert t4 != t6

# # Tests the cancellation of tasks
def test_cancel_task(t_uuid, tm_training_ts, tm_prediction_ts):
    tm_training_ts.cancelTask(t_uuid)
    assert tm_training_ts.getTask(t_uuid).status == Task.Status.CANCELLED.name

    tm_prediction_ts.cancelTask(t_uuid)
    assert tm_prediction_ts.getTask(t_uuid).status == Task.Status.CANCELLED.name

# # Tests the export of the task status
def test_pickle_cancel(tm_training_ts, tm_prediction_ts, ts):
    ts_training_pickled = tm_training_ts.getAllTasksPickled()
    assert ts == jsonpickle.decode(ts_training_pickled)

    ts_prediction_pickled = tm_prediction_ts.getAllTasksPickled()
    assert ts == jsonpickle.decode(ts_prediction_pickled)