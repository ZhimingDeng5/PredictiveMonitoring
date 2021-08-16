import os


def predict(path_to_monitor, path_to_event_log):
    res = []

    predictor_iter = os.scandir(path_to_monitor)
    path_prefix: str = "..\..\\back-end\\"

    for predictor in predictor_iter:
        print(predictor.path)
        cmd: str = f"cd ..\\nirdizati-training-backend\core && set \"PYTHONPATH=..\\\" && python predict_multi.py {path_prefix}{path_to_event_log} {path_prefix}{predictor.path}"
        print(cmd)
        f = os.popen(cmd, "r")
        d = f.read()
        res.append(d)
        f.close()

    print(res)
    return res