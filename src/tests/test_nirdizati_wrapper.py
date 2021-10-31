import sys
sys.path.insert(1, '../')

import os
import multiprocessing as mp
import numpy as np
import pandas as pd
import pytest

from commons.nirdizati_wrapper import predict, train

@pytest.fixture(autouse = True)
def setup_env():
    env_dir = "../commons/nirdizati-training-backend"
    os.environ["PYTHONPATH"] = env_dir
    sys.path.append(env_dir)

    sys.path.insert(0, os.path.join(env_dir, "core"))

# Test the Nirdizati prediction (only output existence, not correctness)
def test_predict(mocker):

    # Return simplified results of predict_multi()
    def mock_predict_multi(path_to_event_log, path_to_predictor):
        print("here")
        if path_to_predictor == os.path.join(predictors, "test-label-predictor.pkl"):
            data = np.array([["1234567890", True, 0.75]])
            df = pd.DataFrame(data, columns = ["Case ID", "label", "probability"])
            return df, {"agg1": 0}
        else:
            data = np.array([["1234567890", "01-01-2021 00:00:00"]])
            df = pd.DataFrame(data, columns = ["Case ID", "predicted-completion"])
            return df, {"agg1": 0, "agg2": 0}

    m_predict = mocker.patch("predict_multi.predict_multi", side_effect = mock_predict_multi)
    
    # Use data samples
    sample_root = os.path.join(os.getcwd(), "..", "..", "DataSamples", "bpi")
    predictors = os.path.join(sample_root, "predictors")
    event_log = os.path.join(sample_root, "test-event-log.parquet")
    save_loc = os.path.join(os.getcwd(), "test_files", "test-predict")
    q = mp.Queue()

    predict(predictors, event_log, save_loc, q)

    assert q.get() == ""

    # Read output file from predict()
    with open(f"{save_loc}-results.csv") as file:
        lines = file.readlines()

        agg_header = lines[0].replace("\n", "")
        agg_result = lines[1].replace("\n", "")
        predict_headers = lines[2].replace("\n", "").split(",")
        predict_results = lines[3].replace("\n", "").split(",")

        assert lines[0] == "agg1,agg2\n"
        assert lines[1] == "0,0\n"
        assert "label" in predict_headers
        assert "probability" in predict_headers
        assert "predicted-completion" in predict_headers
        assert "True" in predict_results
        assert "0.75" in predict_results
        assert "01-01-2021 00:00:00" in predict_results

def test_train(mocker):

    m = mocker.patch("train.train", return_value = True)

    # Use data samples
    sample_root = os.path.join(os.getcwd(), "..", "..", "DataSamples", "bpi")
    config = os.path.join(sample_root, "test-remtime-config.json")
    schema = os.path.join(sample_root, "test-schema.json")
    event_log = os.path.join(sample_root, "test-event-log.parquet")
    save_loc = os.path.join(os.getcwd(), "test_files", "test-train")
    q = mp.Queue()

    train(config, schema, event_log, save_loc, q)

    assert q.get() == ""
    m.assert_called_with(event_log, config, schema, save_loc)