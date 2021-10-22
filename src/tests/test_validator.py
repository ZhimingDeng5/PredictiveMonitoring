import sys
sys.path.insert(1, '../')

import commons.validator as va
import commons.file_handler as fh
import pandas as pd
import pytest


@pytest.fixture
def config_p():
    config_p = "../../DataSamples/bpi/test-remtime-config.json"
    return config_p


@pytest.fixture
def path_p():
    path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    return path_p


@pytest.fixture
def predictor_json():
    path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    predictor_json = fh.pickleLoadingAsDict(path_p)
    return predictor_json


@pytest.fixture
def path_csv_c():
    path_csv_c = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    return path_csv_c


@pytest.fixture
def event_log_json():
    path_c = "../../DataSamples/bpi/test-event-log.csv"
    cf = pd.read_csv(path_c, index_col=False)
    event_log_json = cf.to_json(orient='records')
    return event_log_json


@pytest.fixture
def path_s():
    path_s = "../../DataSamples/bpi/test-schema.json"
    return path_s


@pytest.fixture
def schema_json():
    path_s = "../../DataSamples/bpi/test-schema.json"
    schema_json = open(path_s).read()
    return schema_json


def test_validate_by_schema(event_log_json, schema_json):
    assert va.validate_csv_in_path(event_log_json, schema_json)["isSuccess"]


def test_validate_csv_in_path(path_csv_c, path_s, event_log_json, mocker):
    mocker.patch('services.validator.validate_by_schema', mocker.mock_open(return_value=event_log_json))
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_pickle(predictor_json):
    assert va.validate_pickle(predictor_json)["isSuccess"]


def test_validate_pickle_in_file(path_p, predictor_json, mocker):
    mocker.patch('services.validator.validate_pickle', mocker.mock_open(return_value=predictor_json))
    assert va.validate_pickle_in_path(path_p)["isSuccess"]


def test_type_check():
    assert va.type_check(0, "int")
    assert not va.type_check(0, "float")


def test_check_timestamp():
    timestamp = "2016/10/10 18:27:48"
    assert va.check_timestamp(timestamp)


def validate_config(config_p, path_s):
    assert va.validate_config(config_p, path_s)["isSuccess"]
