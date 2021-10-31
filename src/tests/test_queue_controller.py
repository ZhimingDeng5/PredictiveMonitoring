from commons.service_types import Service
from commons.cancel_request import CancelRequest
from commons.task import Task
from commons import queue_controller as qc
from uuid import uuid4
from mock import patch, Mock
import pika
import sys
sys.path.insert(1, '../')


def dummy_callback(self, channel, method, properties, body):
    pass


@patch.object(pika, 'BlockingConnection')
def test_create_con_chn(con):
    chn = con.return_value.channel

    qc.subscribeToQueue(dummy_callback, "test")

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.queue_declare.assert_called_once_with(
        queue="test", durable=True)
    chn.return_value.basic_qos.assert_called_once_with(prefetch_count=1)
    chn.return_value.basic_consume.assert_called_once_with(
        queue="test", on_message_callback=dummy_callback)


def test_use_passed_con_chn():
    con = Mock()
    chn = Mock()

    retcon, retchn = qc.subscribeToQueue(dummy_callback, "test", con, chn)

    chn.queue_declare.assert_called_once_with(queue="test", durable=True)
    chn.basic_qos.assert_called_once_with(prefetch_count=1)
    chn.basic_consume.assert_called_once_with(
        queue="test", on_message_callback=dummy_callback)
    assert retcon == con
    assert retchn == chn


@patch.object(pika, 'BlockingConnection')
def test_subscribe_named_fanout(con):
    chn = con.return_value.channel
    qc.subscribeToFanout(dummy_callback, "test_fanout", "test")
    expected_queue_name = con.return_value.channel.return_value.queue_declare.return_value.method.queue

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.exchange_declare.assert_called_once_with(
        exchange="test_fanout", exchange_type="fanout")
    chn.return_value.queue_declare.assert_called_once_with(
        queue="test", durable=True)
    chn.return_value.queue_bind.assert_called_once_with(
        exchange="test_fanout", queue=expected_queue_name)
    chn.return_value.basic_consume.assert_called_once_with(
        queue=expected_queue_name, on_message_callback=dummy_callback)


@patch.object(pika, 'BlockingConnection')
def test_subscribe_exclusive_fanout(con):
    chn = con.return_value.channel
    qc.subscribeToFanout(dummy_callback, "test_fanout")
    expected_queue_name = con.return_value.channel.return_value.queue_declare.return_value.method.queue

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.exchange_declare.assert_called_once_with(
        exchange="test_fanout", exchange_type="fanout")
    chn.return_value.queue_declare.assert_called_once_with(
        queue='', exclusive=True)
    chn.return_value.queue_bind.assert_called_once_with(
        exchange="test_fanout", queue=expected_queue_name)
    chn.return_value.basic_consume.assert_called_once_with(
        queue=expected_queue_name, on_message_callback=dummy_callback)


def test_fanout_use_passed_con_chn():
    con = Mock()
    chn = Mock()
    expected_queue_name = chn.queue_declare.return_value.method.queue
    retcon, retchn = qc.subscribeToFanout(
        dummy_callback, "test_fanout", "test", con, chn)

    chn.exchange_declare.assert_called_once_with(
        exchange="test_fanout", exchange_type='fanout')
    chn.queue_declare.assert_called_once_with(queue="test", durable=True)
    chn.queue_bind.assert_called_once_with(
        exchange="test_fanout", queue=expected_queue_name)
    chn.basic_consume.assert_called_once_with(
        queue=expected_queue_name, on_message_callback=dummy_callback)
    assert retcon == con
    assert retchn == chn


def test_return_false_on_nonblocking_requests_when_queue_down():
    con = Mock()
    chn = Mock()
    chn.queue_declare.return_value.method.consumer_count = 0

    ret_val = qc.requestFromQueue("test", "123", False, con, chn)

    chn.queue_declare.assert_called_once_with(queue="test", durable=True)
    con.close.assert_called_once()
    assert ret_val is False


# the following two mocks are very hacky, but I could not come up with
# anything better
def test_handle_request_response():
    con = Mock()
    chn = Mock()
    callback = None
    consume_count = 0
    process_events_count = 0

    def extract_callback(queue, on_message_callback, auto_ack):
        nonlocal callback, consume_count
        callback = on_message_callback
        consume_count += 1

    def process_events():
        nonlocal process_events_count
        callback("", "", Mock(correlation_id="123"), "body")
        process_events_count += 1

    chn.basic_consume = extract_callback

    con.process_data_events = process_events
    ret_val = qc.requestFromQueue("test", "123", True, con, chn)

    chn.queue_declare.assert_called_with(queue='', exclusive=True)
    con.close.assert_called_once()
    assert ret_val == "body"
    assert consume_count == 1
    assert process_events_count == 1


def test_handle_request_response_corr_id_mismatch():
    con = Mock()
    chn = Mock()
    callback = None
    consume_count = 0
    process_events_count = 0
    corr_id = "1"
    body = "b"

    def extract_callback(queue, on_message_callback, auto_ack):
        nonlocal callback, consume_count
        callback = on_message_callback
        consume_count += 1

    def process_events():
        nonlocal process_events_count, corr_id, body
        callback("", "", Mock(correlation_id=corr_id), body)
        process_events_count += 1
        corr_id += "1"
        body += "b"

    chn.basic_consume = extract_callback

    con.process_data_events = process_events
    ret_val = qc.requestFromQueue("test", "1111", True, con, chn)

    chn.queue_declare.assert_called_with(queue='', exclusive=True)
    con.close.assert_called_once()
    assert ret_val == "bbbb"
    assert consume_count == 1
    assert process_events_count == 4


@patch.object(pika, 'BlockingConnection')
def test_create_con_chn(con):
    chn = con.return_value.channel
    task: Task = Task(uuid4(), "", "", "", "", Task.Status.QUEUED)

    qc.sendTaskToQueue(task, "test")

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.basic_publish.assert_called_once_with(
        exchange="",
        routing_key="test",
        body=task.toJsonS(),
        properties=pika.BasicProperties(
            delivery_mode=2))
    con.return_value.close.assert_called_once()


@patch.object(pika, 'BlockingConnection')
def test_send_cancel_request_prediction(con):
    chn = con.return_value.channel
    request: CancelRequest = CancelRequest(uuid4())

    qc.sendCancelRequest(request, "123", Service.PREDICTION)

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.exchange_declare.assert_called_once_with(
        exchange="cancellations_p", exchange_type="fanout")
    chn.return_value.basic_publish.assert_called_once_with(
        exchange="cancellations_p", properties=pika.BasicProperties(
            correlation_id="123"), routing_key="", body=request.toJsonS())
    con.return_value.close.assert_called_once()


@patch.object(pika, 'BlockingConnection')
def test_send_cancel_request_training(con):
    chn = con.return_value.channel
    request: CancelRequest = CancelRequest(uuid4())

    qc.sendCancelRequest(request, "123", Service.TRAINING)

    con.assert_called_once()
    chn.assert_called_once()
    chn.return_value.exchange_declare.assert_called_once_with(
        exchange="cancellations_t", exchange_type="fanout")
    chn.return_value.basic_publish.assert_called_once_with(
        exchange="cancellations_t", properties=pika.BasicProperties(
            correlation_id="123"), routing_key="", body=request.toJsonS())
    con.return_value.close.assert_called_once()
