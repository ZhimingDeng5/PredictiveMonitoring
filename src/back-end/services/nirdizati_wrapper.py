import os
import subprocess
import sys
from sys import argv


def predict(path_to_monitor, path_to_event_log, save_loc):
    # Set paths
    sys.path.insert(0, os.path.join(os.getcwd(), "..\\nirdizati-training-backend\\core"))

    from predict_multi import predict_multi

    predictor_iter = os.scandir(path_to_monitor)
    for predictor in predictor_iter:
        predict_multi(path_to_event_log, predictor.path, save_loc)