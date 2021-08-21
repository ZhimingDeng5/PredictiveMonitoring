import os


def predict(path_to_monitor, path_to_event_log, save_loc):
    res = []

    predictor_iter = os.scandir(path_to_monitor)

    for predictor in predictor_iter:
        # print(predictor.path)
        # cmd: str = f"cd ..\\nirdizati-training-backend\core && set \"PYTHONPATH=..\\\" && python predict_multi.py {path_prefix}{path_to_event_log} {path_prefix}{predictor.path}"
        # print(cmd)
        # f = os.popen(cmd, "r")
        # d = f.read()
        # res.append(d)
        # f.close()
        os.system(f"cd ..\\nirdizati-training-backend\core && set \"PYTHONPATH=..\\\" && python predict_multi.py \"{path_to_event_log}\" \"{predictor.path}\" \"{save_loc}\"")

    print(res)
    return res