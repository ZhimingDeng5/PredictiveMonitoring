import multiprocessing as mp
import os
import sys
import pandas as pd


# Calls the predict_multi function in the Nirdizati code
# for each predictor in the monitor
def predict(path_to_predictors: str, path_to_event_log: str, save_loc: str, q: mp.Queue):
    try:
        # Set path
        sys.path.insert(0, os.path.join("commons", "nirdizati-training-backend", "core"))

        from predict_multi import predict_multi

        combined_results = pd.DataFrame()
        aggregate_data = {}
        init_results = True

        predictor_iter = os.scandir(path_to_predictors)
        for predictor in predictor_iter:
            predictor_result, predictor_aggregate = predict_multi(path_to_event_log, predictor.path)

            # Either start with results or append to existing
            if init_results:
                combined_results = predictor_result
                init_results = False
            else:
                combined_results = pd.merge(combined_results, predictor_result, on = "Case ID")
            
            # Only save if new aggregate info (remtime provides the most)
            if len(predictor_aggregate) > len(aggregate_data):
                aggregate_data = predictor_aggregate
        
        aggregate_data = pd.DataFrame([aggregate_data])
        aggregate_data.to_csv(f"{save_loc}-results.csv", sep=",", index=False)
        combined_results.to_csv(f"{save_loc}-results.csv", mode="a", sep=",", index=False)

        print("Wrapper succeeded")
        q.put("")
    except Exception as e:
        print(f"Wrapper failed with exception: {repr(e)}")
        q.put(repr(e))


def train(path_to_config: str, path_to_schema: str, path_to_event_log: str, save_loc: str, q: mp.Queue):
    try:
        # Set path
        sys.path.insert(0, os.path.join("commons", "nirdizati-training-backend", "core"))

        from train import train

        train(path_to_event_log, path_to_config, path_to_schema, save_loc)

        print("Wrapper succeeded")
        q.put("")
    except Exception as e:
        print(f"Wrapper failed with exception: {repr(e)}")
        q.put(repr(e))