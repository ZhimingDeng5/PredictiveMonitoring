from commons.service_types import Service
from commons.cancellation_handler import CancellationHandler
from uuid import UUID, uuid4
import pytest
import os
import jsonpickle
import sys
sys.path.insert(1, '../')


@pytest.fixture
def t_uuid():
    t_uuid = uuid4()
    return t_uuid


@pytest.fixture
def cs(t_uuid):
    cs = {t_uuid}
    return cs


@pytest.fixture
def ch_training():
    ch_training = CancellationHandler(Service.TRAINING)
    return ch_training


@pytest.fixture
def ch_prediction():
    ch_prediction = CancellationHandler(Service.PREDICTION)
    return ch_prediction


# Tests the proper initialisation of the CancellationHandler
def test_init(ch_training, ch_prediction):
    assert ch_training.getCurrentTask() == UUID(
        "00000000-0000-0000-0000-000000000000")
    assert ch_prediction.getCurrentTask() == UUID(
        "00000000-0000-0000-0000-000000000000")

    assert ch_training.isEmpty()
    assert ch_prediction.isEmpty()


# Tests the proper current task setting
def test_set_task(t_uuid, ch_training, ch_prediction):
    ch_training.setCurrentTask(t_uuid)
    assert ch_training.getCurrentTask() == t_uuid

    ch_prediction.setCurrentTask(t_uuid)
    assert ch_prediction.getCurrentTask() == t_uuid


# Tests the addition of a cancel request
def test_add_cancel(t_uuid, ch_training, ch_prediction):
    ch_training.addCancel(t_uuid)
    assert ch_training.hasCancel(t_uuid)
    assert not ch_training.isEmpty()

    ch_prediction.addCancel(t_uuid)
    assert ch_prediction.hasCancel(t_uuid)
    assert not ch_prediction.isEmpty()


# Tests the removal of a cancel request
def test_remove_cancel(t_uuid, ch_training, ch_prediction):
    ch_training.addCancel(t_uuid)
    ch_training.removeCancel(t_uuid)
    assert not ch_training.hasCancel(t_uuid)
    assert ch_training.isEmpty()

    ch_prediction.addCancel(t_uuid)
    ch_prediction.removeCancel(t_uuid)
    assert not ch_prediction.hasCancel(t_uuid)
    assert ch_prediction.isEmpty()


# Tests the export of the cancel set
def test_pickle_cancel(t_uuid, ch_training, ch_prediction):
    ch_training.addCancel(t_uuid)
    cs_training_pickled = ch_training.getAllCancelPickled()
    cs_training = jsonpickle.decode(cs_training_pickled)
    assert t_uuid in cs_training

    ch_prediction.addCancel(t_uuid)
    cs_prediction_pickled = ch_prediction.getAllCancelPickled()
    cs_prediction = jsonpickle.decode(cs_prediction_pickled)
    assert t_uuid in cs_prediction


# Tests the reading and writing from the cancel set on disk
def test_write_to_disk(t_uuid, ch_training, ch_prediction, cs, mocker):
    m = mocker.patch("builtins.open", mocker.mock_open())
    data = jsonpickle.encode(cs)

    ch_training.addCancel(t_uuid, persist=True)
    m.assert_called_with("../persistence/cancel_set_t", "w+")
    handle = m()
    handle.write.assert_called_with(data)

    ch_prediction.addCancel(t_uuid, persist=True)
    m.assert_called_with("../persistence/cancel_set_p", "w+")
    handle = m()
    handle.write.assert_called_with(data)


# Tests updating own cancel set from disk
def test_update_from_disk(t_uuid, ch_training, ch_prediction, cs, mocker):
    data = jsonpickle.encode(cs)
    m_check = mocker.patch("os.path.isfile", return_value=True)
    m_read = mocker.patch(
        "builtins.open", mocker.mock_open(read_data=str(data)))

    ch_training.getStateFromDisk()
    assert ch_training.hasCancel(t_uuid)

    ch_prediction.getStateFromDisk()
    assert ch_prediction.hasCancel(t_uuid)


# Tests updating own cancel set from network
# def test_state_from_network():
