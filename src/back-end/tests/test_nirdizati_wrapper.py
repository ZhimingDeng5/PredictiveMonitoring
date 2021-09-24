import datetime
import os
import pandas as pd
import pytest
import sys

from services.nirdizati_wrapper import predict

@pytest.fixture(autouse = True)
def setup_environment():
    env_dir = "nirdizati-training-backend"
    os.environ["PYTHONPATH"] = env_dir
    sys.path.append(env_dir)
    sys.path.insert(0, os.path.join(env_dir, "core"))

# Test the Nirdizati wrapper
def test_predict(mocker):
    # Fake prediction results
    now = datetime.datetime.now()
    delta = now - now
    data = [[1234, True, 0.8, now]]
    predictor_result = pd.DataFrame(data, columns = ["Case ID", "Label", "probability", "predicted-completion"])
    aggregates = [[1000, 500, 500, 10, 1, 100, 10, now, now, delta, delta, delta, delta]]
    aggregate_data = pd.DataFrame(aggregates, columns = ["Total cases", "Running cases", "Completed cases", "Case variants", "Average case length", "Completed events", "Activities", "Start of log", "End of log", "Min. case duration", "Median case duration", "Average case duration", "Max. case duration"])

    # Test file paths
    sample_root = os.path.join("..", "..", "DataSamples", "bpi")
    predictors = os.path.join(sample_root, "predictors")
    event_log = os.path.join(sample_root, "test-event-log.csv")
    save_loc = os.path.join(sample_root, "test-prediction")

    # mocker.patch("services.nirdizati_wrapper.predict_multi", return_value = (predictor_result, aggregate_data))
    # m_result = mocker.patch.object(predictor_result, "to_csv")
    # m_aggregate = mocker.patch.object(aggregate_data, "to_csv")
    # predict(predictors, event_log, save_loc)
    
    # m_result.assert_called_once_with(f"{save_loc}-results.csv", ",", False)
    # m_aggregate.assert_called_once_with(f"{save_loc}-results.csv", "a", ",", False)