import commons.file_handler as fh
import json
import os
import pandas as pd

import sys
sys.path.insert(0, os.path.join("commons", "nirdizati-training-backend"))
sys.path.insert(0, os.path.join("commons", "nirdizati-training-backend", "core"))


# This validation is used to check the type of each object which is based on the template.
def validate_pickle(data):
    try:
        for index, Pipeline in data.items():
            if not type_check(index, ["int"]):
                return response(False, str(type(index)) + " is not int")
            if not type_check(Pipeline, ["Pipeline"]):
                return response(False, str(type(Pipeline)) + " is not Pipeline")
            for step in Pipeline.steps:
                step_name = step[0]
                if step_name not in ["encoder", "cls"]:
                    return response(False, step_name + " is not static or agg")
                if step_name == "encoder":
                    if not type_check(step[1], ["FeatureUnion"]):
                        return response(False, str(type(step[1])) + " is not FeatureUnion")
                    for transformer_item in step[1].transformer_list:
                        transformer_name = transformer_item[0]
                        if transformer_name not in ["static", "agg"]:
                            return response(False, transformer_name + " is not static or agg")
                        if transformer_name == "static":
                            if not type_check(transformer_item[1], ["StaticTransformer"]):
                                return response(False, str(type(transformer_item[1])) + " is not StaticTransformer")
                        elif transformer_name == "agg":
                            if not type_check(transformer_item[1], ["AggregateTransformer"]):
                                return response(False, str(type(transformer_item[1])) + " is not AggregateTransformer")
                elif step_name == "cls":
                    if not type_check(step[1], ["ClassifierWrapper"]):
                        return response(False, str(type(step[1])) + " is not ClassifierWrapper")
        return response(True, "correct label pickle file")
    except Exception as e:
        return response(False, "wrong pickle file structure: "+ str(e))


def validate_pickle_in_path(path_str):
    try:
        data = fh.pickleLoadingAsDict(path_str)
        return validate_pickle(data)
    except Exception as e:
        return response(False, "wrong pickle file structure: " + str(e))


# check the single type
def type_check(obj, ts):
    for t in ts:
        if obj is not None and t not in str(type(obj)):
            return False
    return True


# used for validating the event log (csv) file by schema
def validate_csv_in_path(csv_path: str, schema_path: str):
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            first_line = lines[0]
        de = ","
        if first_line.count(";") > first_line.count(","):
            de = ";"
        cf = pd.read_csv(csv_path, index_col=False, low_memory=False, delimiter=de, nrows=200)
        types = cf.dtypes
        schema = open(schema_path).read()
        params_json = json.loads(schema)
        items = params_json.items()
    except Exception as e:
        return response(False, "validator error: " + str(e))
    try:
        for key, value in items:
            # schema item with a list of cols
            if str(value).find('[') != -1:
                for name in list(value):
                    if str(key).lower().find('num') != -1 or str(key).lower().find('ignore') != -1:
                        if types[name] is None or (types[name] != "int64" and types[name] != "float64"):
                            return response(False, '\"' + str(name) + '\" should be a number')
                    elif str(key).lower().find('timestamp') != -1:
                        if types[name] is None or not check_timestamp(cf[name]):
                            return response(False, '\"' + str(name) + '\" should be a timestamp')
                    else:
                        if types[name] is None or \
                                (types[name] != "object" and types[name] != "int64" and
                                 types[name] != "float64" and types[name] != "bool"):
                            return response(False, '\"' + str(name) + '\" should be a object')
            else:
                name = value
                if str(key).lower().find('num') != -1 or str(key).lower().find(
                        'ignore') != -1:
                    if types[name] is None or (types[name] != "int64" and types[name] != "float64"):
                        return response(False, '\"' + str(name) + '\" should be a number')
                elif str(key).lower().find('timestamp') != -1:
                    if types[name] is None or not check_timestamp(cf[name]):
                        return response(False, '\"' + str(name) + '\" should be a timestamp')
                else:
                    if types[name] is None or \
                            (types[name] != "object" and types[name] != "int64" and
                             types[name] != "float64" and types[name] != "bool"):
                        return response(False, '\"' + str(name) + '\" should be a object')
        return response(True, "correct")
    except Exception as e:
        return response(False, "Missing col: "+str(e))


# check the timestamp
def check_timestamp(timestamp):
    try:
        if "datetime64" in str(pd.to_datetime(timestamp).dtype):
            return True
        else:
            return False
    except Exception as e:
        return False


# generate a response
def response(status: bool, msg: str):
    return {'isSuccess': status, 'msg': msg}


# check the config files
def validate_config(config_path: str, schema_path: str):
    try:
        config_str = open(config_path).read()
        config_json = json.loads(config_str)
        target_key = list(config_json.keys())[0]
        if len(config_json) > 3:
            return response(False, "config file should only have two or three attributes")
        schema = open(schema_path).read()
        schema_json = json.loads(schema)

        if target_key != "remtime" and \
                target_key not in schema_json["static_cat_cols"] and \
                target_key not in schema_json["static_num_cols"]:
            return response(False, target_key + " is not a parameter of config json")
        bucket = config_json[target_key]
        if len(bucket) != 1:
            return response(False, target_key + " should only have one attribute")
        bucketing_type = list(bucket.keys())[0]
        if bucketing_type not in ["zero", "cluster", "state", "prefix"]:
            return response(False, bucketing_type + " is not a parameter of a bucket")
        is_cluster = False
        if bucketing_type == "cluster":
            is_cluster = True
        encoding = bucket[bucketing_type]
        if len(encoding) != 1:
            return response(False, bucketing_type + " should only have one attribute")
        encoding_type = list(encoding.keys())[0]
        if encoding_type not in ["agg", "laststate", "index", "combined"]:
            return response(False, encoding_type + " is not a parameter of an encoding")
        learner = encoding[encoding_type]
        if len(learner) != 1:
            return response(False, encoding_type + " should only have one attribute")
        learner_type = list(learner.keys())[0]
        l_v = learner[learner_type]
        if learner_type == "rf":
            if is_cluster and len(l_v) != 3:
                return response(False, learner_type + " should only have three attributes")
            if not is_cluster and len(l_v) != 2:
                return response(False, learner_type + " should only have two attributes")
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_features"]:
                    return response(False, p + " is not a parameter of " + learner_type)
                if "float" not in str(type(p_v)) and "int" not in str(type(p_v)):
                    return response(False, p + " should be a number")
        elif learner_type == "gbm":
            if is_cluster and len(l_v) != 4:
                return response(False, learner_type + " should only have four attributes")
            if not is_cluster and len(l_v) != 3:
                return response(False, learner_type + " should only have three attributes")
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_features", "learning_rate"]:
                    return response(False, p + " is not a parameter of " + learner_type)
                if "float" not in str(type(p_v)) and "int" not in str(type(p_v)):
                    return response(False, p + " should be a number")
        elif learner_type == "dt":
            if is_cluster and len(l_v) != 3:
                return response(False, learner_type + " should only have three attributes")
            if not is_cluster and len(l_v) != 2:
                return response(False, learner_type + " should only have two attributes")
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "max_features", "max_depth"]:
                    return response(False, p + " is not a parameter of " + learner_type)
                if "float" not in str(type(p_v)) and "int" not in str(type(p_v)):
                    return response(False, p + " should be a number")
        elif learner_type == "xgb":
            if is_cluster and len(l_v) != 6:
                return response(False, learner_type + " should only have six attributes")
            if not is_cluster and len(l_v) != 5:
                return response(False, learner_type + " should only have five attributes")
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_depth", "learning_rate", "colsample_bytree", "subsample"]:
                    return response(False, p + " is not a parameter of " + learner_type)
                if "float" not in str(type(p_v)) and "int" not in str(type(p_v)):
                    return response(False, p + " should be a number")
        else:
            return response(False, learner_type + " is not a parameter of learner")
        return response(True, "config file is correct")
    except Exception as e:
        return response(False, str(e))
