import sys
sys.path.insert(1, '../')

import commons.validator as va
import commons.file_handler as fh
import pandas as pd


config_p = "../../DataSamples/bpi/test-remtime-config.json"
path_p = "../../DataSamples/bpi/predictors/test-label-predictor.pkl"
predictor_json = fh.pickleLoadingAsDict(path_p)
path_csv_c = "../../DataSamples/bpi/test-event-log.csv"
event_log_json = pd.read_csv(path_csv_c, index_col=False, low_memory=False, nrows=200)
path_par_c = "../../DataSamples/bpi/test-event-log.parquet"
path_s = "../../DataSamples/bpi/test-schema.json"
schema_json = open(path_s).read()


def test_validate_by_schema():
    assert va.validate_csv_in_path(event_log_json, schema_json)["isSuccess"]


def test_validate_csv_in_path():
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_parquet_in_path():
    assert va.validate_parquet_in_path(path_par_c, path_s)["isSuccess"]


def test_validate_pickle():
    assert va.validate_pickle(predictor_json)["isSuccess"]


def test_validate_pickle_in_file():
    assert va.validate_pickle_in_path(path_p)["isSuccess"]


def test_type_check():
    assert va.type_check(0, "int")
    assert not va.type_check(0, "float")


def test_check_timestamp():
    timestamp = "2016/10/10 18:27:48"
    assert va.check_timestamp(timestamp)


def validate_config():
    assert va.validate_config(config_p, path_s)["isSuccess"]
