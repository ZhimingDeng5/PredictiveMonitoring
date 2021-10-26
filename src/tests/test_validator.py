import sys
sys.path.insert(1, '../')

import commons.validator as va
import pickle
import os


# set up the test env
env_dir = "../commons/nirdizati-training-backend"
os.environ["PYTHONPATH"] = env_dir
sys.path.append(env_dir)
sys.path.insert(0, os.path.join(env_dir, "core"))


# inputs
config_p = "../../DataSamples/bpi/test-remtime-config.json"
path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
predictor_json = pickle.load(open(path_p, 'rb'))
path_csv_c = "../../DataSamples/bpi/test-event-log.csv"
path_par_c = "../../DataSamples/bpi/test-event-log.parquet"
path_s = "../../DataSamples/bpi/test-schema.json"


def test_validate_csv_in_path():
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_parquet_in_path():
    assert va.validate_parquet_in_path(path_par_c, path_s)["isSuccess"]


def test_validate_pickle():
    assert va.validate_pickle(predictor_json)["isSuccess"]


def test_validate_pickle_in_path():
    assert va.validate_pickle_in_path(path_p)["isSuccess"]


def test_type_check():
    assert va.type_check(0, "int")
    assert not va.type_check(0, "float")


def validate_config():
    assert va.validate_config(config_p, path_s)["isSuccess"]
