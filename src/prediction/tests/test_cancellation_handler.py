import jsonpickle
import pytest
from uuid import UUID, uuid4

from commons.cancellation_handler import CancellationHandler


@pytest.fixture
def ch():
    ch = CancellationHandler("cancel_set_request_p")
    return ch

# Tests the proper initialisation of the CancellationHandler
def test_init(ch):
    assert ch.getCurrentTask() == UUID("00000000-0000-0000-0000-000000000000")
    assert ch.isEmpty()

# Tests the proper current task setting
def test_set_task(ch):
    task_uuid = uuid4()
    ch.setCurrentTask(task_uuid)
    assert ch.getCurrentTask() == task_uuid

# Tests the addition of a cancel request
def test_add_cancel(ch):
    task_uuid = uuid4()
    ch.addCancel(task_uuid)
    assert ch.hasCancel(task_uuid)
    assert not ch.isEmpty()

# Tests the removal of a cancel request
def test_remove_cancel(ch):
    task_uuid = uuid4()
    ch.addCancel(task_uuid)
    ch.removeCancel(task_uuid)
    assert not ch.hasCancel(task_uuid)
    assert ch.isEmpty()

# Tests the export of the cancel set
def test_pickle_cancel(ch):
    task_uuid = uuid4()
    ch.addCancel(task_uuid)
    cs_pickled = ch.getAllCancelPickled()
    cs = jsonpickle.decode(cs_pickled)
    assert task_uuid in cs

# Tests the reading and writing from the cancel set on disk
def test_read_write_to_disk(ch):
    task_uuid = uuid4()
    ch.addCancel(task_uuid, persist = True)

    with open("../persistence/cancel_set", "r") as f:
        cs_pickled = f.read()
        cs = jsonpickle.decode(cs_pickled)
        assert task_uuid in cs

# Tests updating own cancel set from disk
def test_update_from_disk(ch):
    task_uuid = uuid4()
    ch.addCancel(task_uuid, persist = True)

    ch2 = CancellationHandler("cancel_set_request_p")
    ch2.getStateFromDisk()
    assert ch2.hasCancel(task_uuid)

# Tests updating own cancel set from network
# def test_state_from_network():