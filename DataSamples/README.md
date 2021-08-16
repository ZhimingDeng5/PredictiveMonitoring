# Data samples

This folder contains examples of all relevant input and output files as part of the prediction/training process.

Filename | Description | Usage
-------- | ----------- | -----
bpi17_sample_event.json | JSON formatted trace of single event from event log | Input as argument for Nirdizati's predict_trace.py
bpi17_sample.csv | Event log | Input as argument for Nirdizati's predict_multi.py
bpi17_sample_schema.json | Event log schema | Used for validation of the event log
bpi17_sample_myconfig_label.pkl | Predictor used for event labels | Input as argument for either prediction module
bpi17_sample_myconfig_remtime.pkl | Predictor used for event remaining time | Input as argument for either prediction module
results_bpi17_sample.csv_remtime.csv | Resulting remaining time predictions | Output from predict_multi.py