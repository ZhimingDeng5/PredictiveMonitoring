import os
import sys

import pandas as pd


# Calls the predict_multi function in the Nirdizati code
# for each predictor in the monitor
def predict(path_to_predictors: str, path_to_event_log: str, save_loc: str):
    # Set path
    sys.path.insert(0, os.path.join("nirdizati-training-backend", "core"))

    from predict_multi import predict_multi

    combined_results = pd.DataFrame()
    init_results = True

    predictor_iter = os.scandir(path_to_predictors)
    for predictor in predictor_iter:
        predictor_result, aggregate_data = predict_multi(path_to_event_log, predictor.path, save_loc)
        if init_results:
            combined_results = predictor_result
            init_results = False
        else:
            combined_results = pd.merge(combined_results, predictor_result, on = "Case ID")
    
    aggregate_data = pd.DataFrame([aggregate_data])
    aggregate_data.to_csv(f"{save_loc}-results.csv", sep=",", index=False)
    combined_results.to_csv(f"{save_loc}-results.csv", mode="a", sep=",", index=False)

def train(path_to_config: str, path_to_schema: str, path_to_event_log: str, save_loc: str):
    # Set path
    sys.path.insert(0, os.path.join("nirdizati-training-backend", "core"))

    from train import train

    train(path_to_event_log, path_to_config, path_to_schema, save_loc)