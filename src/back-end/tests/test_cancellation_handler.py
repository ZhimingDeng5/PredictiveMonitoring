import jsonpickle
import pytest
from uuid import UUID, uuid4

from services.cancellation_handler import CancellationHandler


@pytest.fixture
def ch():
    ch = CancellationHandler()
    return ch

@pytest.fixture
def task_uuid():
    task_uuid = uuid4()
    return task_uuid

@pytest.fixture
def cancel_set(task_uuid):
    cancel_set = jsonpickle.encode({task_uuid})
    return cancel_set

# Tests the proper initialisation of the CancellationHandler
def test_init(ch):
    assert ch.getCurrentTask() == UUID("00000000-0000-0000-0000-000000000000")
    assert ch.isEmpty()

# Tests the proper current task setting
def test_set_task(ch, task_uuid):
    ch.setCurrentTask(task_uuid)
    assert ch.getCurrentTask() == task_uuid

# Tests the addition of a cancel request
def test_add_cancel(ch, task_uuid):
    ch.addCancel(task_uuid)
    assert ch.hasCancel(task_uuid)
    assert not ch.isEmpty()

# Tests the removal of a cancel request
def test_remove_cancel(ch, task_uuid):
    ch.addCancel(task_uuid)
    ch.removeCancel(task_uuid)
    assert not ch.hasCancel(task_uuid)
    assert ch.isEmpty()

# Tests the export of the cancel set
def test_pickle_cancel(ch, task_uuid):
    ch.addCancel(task_uuid)
    cs_pickled = ch.getAllCancelPickled()
    cs = jsonpickle.decode(cs_pickled)
    assert task_uuid in cs

# Tests the writing to the cancel set on disk
def test_write_to_disk(ch, task_uuid, cancel_set, mocker):
    m = mocker.patch('builtins.open', mocker.mock_open())
    ch.addCancel(task_uuid, persist = True)
    
    m.assert_called_once_with("../persistence/cancel_set", "w+")
    handle = m()
    handle.write.assert_called_once_with(cancel_set)

# Tests updating own cancel set from disk
def test_update_from_disk(ch, task_uuid, cancel_set, mocker):
    m = mocker.patch('builtins.open', mocker.mock_open(read_data = cancel_set))
    ch.getStateFromDisk()

    m.assert_called_once_with("../persistence/cancel_set", "r")
    assert ch.hasCancel(task_uuid)

# Tests updating own cancel set from network
def test_state_from_network(ch, task_uuid, cancel_set, mocker):
    m = mocker.patch('services.cancellation_handler.requestFromQueue', return_value = cancel_set)
    ch.getStateFromNetwork()

    m.assert_called_once_with("cancel_set_request", ch.corr_id, True)
    assert ch.hasCancel(task_uuid)