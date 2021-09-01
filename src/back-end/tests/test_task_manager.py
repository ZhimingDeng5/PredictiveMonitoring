import jsonpickle
import os
import pytest
from uuid import UUID, uuid4

from services.task import Task
from services.task_manager import TaskManager


# Task format:
# ts = {"00000000-0000-0000-0000-000000000000": {"py/object": "services.task.Task", "taskID": "00000000-0000-0000-0000-000000000000", "predictors_path": "task_files\\00000000-0000-0000-0000-000000000000-predictors", "schema_path": "task_files\\00000000-0000-0000-0000-000000000000-schema", "event_log_path": "task_files\\00000000-0000-0000-0000-000000000000-event_log", "status": "COMPLETED"}}
t_id = "00000000-0000-0000-0000-000000000000"
t_uuid = UUID(t_id)


@pytest.fixture
def tm():
    tm = TaskManager()
    return tm

@pytest.fixture
def ts():
    ts = {t_id: Task(t_id, "", "", "", Task.Status.QUEUED)}
    return ts

@pytest.fixture(autouse = True)
def maintain_task_status(ts):
    # Save current task_status before each task
    with open(os.path.join("..", "persistence", "task_status"), "r") as f_in:
        old_ts = jsonpickle.decode(f_in.read())
    with open(os.path.join("..", "persistence", "task_status"), "w") as f_out_test:
        f_out_test.write(jsonpickle.encode(ts))

    # Perform test
    yield
    
    # Rewrite old task_status after each task
    with open(os.path.join("..", "persistence", "task_status"), "w") as f_out:
        f_out.write(jsonpickle.encode(old_ts))


# Tests the proper initialisation of the CancellationHandler
def test_init(tm):
    assert tm.getAllTasks() == {"tasks": []}

# Tests updating own task_status from disk
def test_update_from_disk(tm):
    tm.getStateFromDisk()
    assert tm.hasTask(t_uuid)

# Tests the removal of tasks
def test_remove_task(tm):
    tm.getStateFromDisk()
    tm.removeTask(t_uuid)
    assert not tm.hasTask(t_uuid)
    assert tm.getAllTasks() == {"tasks": []}

# Tests the update of tasks
def test_update_task(tm):
    tm.getStateFromDisk()
    t1 = tm.getTask(t_uuid)
    t2 = Task(t_id, "", "", "", Task.Status.PROCESSING)
    tm.updateTask(t2)
    t3 = tm.getTask(t_uuid)
    assert t1 != t3

# Tests the cancellation of tasks
def test_cancel_task(tm):
    tm.getStateFromDisk()
    tm.cancelTask(t_uuid)
    assert tm.getTask(t_uuid).status == Task.Status.CANCELLED.name

# Tests the export of the task status
def test_pickle_cancel(tm, ts):
    tm.getStateFromDisk()
    ts_pickled = tm.getAllTasksPickled()
    assert ts == jsonpickle.decode(ts_pickled)