import services.validator as va
import commons.file_handler as fh
import pandas as pd
import json
import copy


def validator_test():
    # Correct pickle file
    path_p = "../../../DataSamples/bpi/predictors/test-label-predictor.pkl"
    json_p = fh.pickleLoadingAsDict(path_p)

    # Wrong pickle file
    json_p_w = copy.deepcopy(json_p)
    json_p_w[0] = 1

    # Corrext CSV file
    path_c = "../../../DataSamples/bpi/test-event-log.csv"
    cf = pd.read_csv(path_c, index_col=False)
    json_c = cf.to_json(orient='records')
    path_json = "../../../DataSamples/bpi/test-single-event.json"

    # Wrong CSV file
    json_c_w = copy.deepcopy(json_c)
    params_json = json.loads(json_c_w)
    params_json[0]["Case ID"] = "test"
    json_c_w = json.dumps(params_json)

    # Schema file
    path_s = "../../../DataSamples/bpi/test-schema.json"
    json_s = open(path_s).read()

    # Perform test
    test_validate_pickle(json_p, json_p_w)
    test_validate_pickle_in_file(path_p)
    test_type_check()
    test_validate_csv_in_path(path_c, path_s)
    test_validate_json_in_path(path_json, path_s)
    test_validate_by_schema(json_c, json_c_w, json_s)
    test_check_timestamp()


def test_validate_pickle(data, data_w):
    assert va.validate_pickle(data)["isSuccess"]
    assert not va.validate_pickle(data_w)["isSuccess"]


def test_validate_pickle_in_file(path):
    assert va.validate_pickle_in_path(path)["isSuccess"]


def test_type_check():
    num = 0
    assert va.type_check(num, "int")
    assert not va.type_check(num, "float")


def test_validate_csv_in_path(path_csv_c, path_s):
    assert va.validate_csv_in_path(path_csv_c, path_s)["isSuccess"]


def test_validate_json_in_path(path_json_c, json_s):
    assert va.validate_json_in_path(path_json_c, json_s)["isSuccess"]


def test_validate_by_schema(json_c, json_c_w, json_s):
    assert va.validate_by_schema(json_c, json_s)["isSuccess"]
    assert not va.validate_by_schema(json_c_w, json_s)["isSuccess"]


def test_check_timestamp():
    timestamp = "2016/10/10 18:27:48"
    assert va.check_timestamp(timestamp)


validator_test()
