import os
import pandas as pd
import pytest
import sys

from services.nirdizati_wrapper import predict


# Test the Nirdizati wrapper
def test_predict(mocker):
    # Setup environment
    env_dir = "nirdizati-training-backend"
    os.environ["PYTHONPATH"] = env_dir
    sys.path.append(env_dir)

    # mocker.patch(
    #    "services.nirdizati_wrapper" 
    # )

    # sample_root = os.path.join("..", "..", "DataSamples", "bpi")
    # predictors = os.path.join(sample_root, "predictors")
    # event_log = os.path.join(sample_root, "test-event-log.csv")
    # save_loc = os.path.join(sample_root, "test-prediction")

    # predict(predictors, event_log, save_loc)
    # prediction = pd.read_csv(f"{save_loc}-results.csv")
    # assert "label" in prediction.columns
    # assert "probability" in prediction.columns
    # assert "predicted-completion" in prediction.columns