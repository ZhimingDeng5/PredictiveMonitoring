import sys
sys.path.insert(1, '../')
import os
import pickle
import pandas as pd
import numpy as np
import pytest
import commons.validator as va


@pytest.fixture(autouse=True)
def setup_env():
    env_dir = "../commons/nirdizati-training-backend"
    os.environ["PYTHONPATH"] = env_dir
    sys.path.append(env_dir)

    sys.path.insert(0, os.path.join(env_dir, "core"))


@pytest.fixture
def config_remtime_p():
    config_p = "../../DataSamples/bpi/test-remtime-config.json"
    return config_p


@pytest.fixture
def config_label_p():
    config_p = "../../DataSamples/bpi/test-label-config.json"
    return config_p


@pytest.fixture
def path_p():
    path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    return path_p


@pytest.fixture
def predictor_json():
    path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    predictor_json = pickle.load(open(path_p, 'rb'))
    return predictor_json


@pytest.fixture
def path_csv_c():
    path_csv_c = "../../DataSamples/bpi/test-event-log.csv"
    return path_csv_c


@pytest.fixture
def path_par_c():
    path_par_c = "../../DataSamples/bpi/test-event-log.parquet"
    return path_par_c


@pytest.fixture
def path_s():
    path_s = "../../DataSamples/bpi/test-schema.json"
    return path_s


def test_validate_csv_in_path(path_csv_c, path_s):
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_parquet_in_path(path_par_c, path_s):
    assert va.validate_parquet_in_path(path_par_c, path_s)["isSuccess"]


def test_validate_pickle(predictor_json):
    assert va.validate_pickle(predictor_json)["isSuccess"]


def test_validate_pickle_in_file(path_p):
    assert va.validate_pickle_in_path(path_p)["isSuccess"]


# check the timestamp
def test_check_timestamp():
    data = np.array(["01-01-2021 00:00:00"])
    cf = pd.DataFrame(data, columns=["timestamp"])
    timestamp = cf["timestamp"]
    assert va.check_timestamp(timestamp)


def test_type_check():
    assert va.type_check(0, "int")
    assert not va.type_check(0, "float")


def test_validate_config(config_remtime_p, config_label_p, path_s):
    assert va.validate_config(config_remtime_p, path_s)["isSuccess"]
    assert va.validate_config(config_label_p, path_s)["isSuccess"]
