import os


def make_predictions(path_to_predictors, path_to_event_log):
    predictors_list = []
    res = []
    for root, dirs, files in os.walk(path_to_predictors):
        for file in files:
            predictors_list.append(os.path.join(root, file))
    # print(predictors_list)
    for predictors in predictors_list:
        cmd='cd..&&cd..&&cd nirdizati-training-backend&&cd core&&python predict_multi.py '+path_to_event_log+' '+predictors
        # print(cmd)
        f = os.popen(cmd, "r")
        d = f.read()
        res.append(d)
        f.close()
    return res



