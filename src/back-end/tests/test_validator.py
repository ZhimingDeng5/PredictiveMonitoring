import pytest

import services.validator as va
import services.file_handler as fh
import pandas as pd


@pytest.fixture
def predictor_json():
    # Correct pickle file
    path_p = "../../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    json_p = fh.pickleLoadingAsDict(path_p)
    return json_p


@pytest.fixture
def event_log_json():
    path_c = "../../../DataSamples/bpi/test-event-log.csv"
    cf = pd.read_csv(path_c, index_col=False)
    json_c = cf.to_json(orient='records')
    return json_c


@pytest.fixture
def schema_json():
    path_s = "../../../DataSamples/bpi/test-schema.json"
    json_s = open(path_s).read()
    return json_s


def test_validate_by_schema(json_c, json_c_w, json_s):
    assert va.validate_by_schema(json_c, json_s)["isSuccess"]
    assert not va.validate_by_schema(json_c_w, json_s)["isSuccess"]


def test_validate_csv_in_path(path_csv_c, path_s, event_log_json, mocker):
    mocker.patch('services.validator.validate_by_schema', mocker.mock_open(return_value=event_log_json))
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_json_in_path(path_json_c, json_s,event_log_json, mocker):
    mocker.patch('services.validator.validate_by_schema', mocker.mock_open(return_value=event_log_json))
    assert va.validate_json_in_path(path_json_c, json_s)["isSuccess"]


def test_validate_pickle(data, data_w):
    assert va.validate_pickle(data)["isSuccess"]
    assert not va.validate_pickle(data_w)["isSuccess"]


def test_validate_pickle_in_file(path, predictor_json, mocker):
    mocker.patch('services.validator.validate_pickle', mocker.mock_open(return_value=predictor_json))
    assert va.validate_pickle_in_path(path)["isSuccess"]


def test_type_check():
    assert va.type_check(0, "int")
    assert not va.type_check(0, "float")


def test_check_timestamp():
    timestamp = "2016/10/10 18:27:48"
    assert va.check_timestamp(timestamp)