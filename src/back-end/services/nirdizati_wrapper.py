import os
import subprocess
import sys
from sys import argv

import pandas as pd


def predict(path_to_predictors, path_to_event_log, save_loc):
    # Set path
    sys.path.insert(0, os.path.join(os.getcwd(), "..\\nirdizati-training-backend\\core"))

    from predict_multi import predict_multi

    combined_results = pd.DataFrame()
    init_results = True

    predictor_iter = os.scandir(path_to_predictors)
    for predictor in predictor_iter:
        predictor_result = predict_multi(path_to_event_log, predictor.path, save_loc)
        if init_results:
            combined_results = predictor_result
            init_results = False
        else:
            combined_results = pd.merge(combined_results, predictor_result, on = "Case ID")
    
    combined_results.to_csv(f"{save_loc}-results.csv", sep=",", index=False)