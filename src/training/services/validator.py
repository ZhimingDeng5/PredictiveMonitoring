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
        cf = pd.read_csv(csv_path, index_col=False)
        s = cf.to_json(orient='records')
        schema = open(schema_path).read()
        return validate_by_schema(s, schema)
    except Exception as e:
        return response(False, "Wrong type for csv file or schema file: "+str(e))


# used for validating the event log (json) file by schema
def validate_json_in_path(json_path: str, schema_path: str):
    try:
        jf = pd.read_json(json_path)
        s = jf.to_json(orient='records')
        schema = open(schema_path).read()
        return validate_by_schema(s, schema)
    except Exception as e:
        return response(False, "Wrong type for json file or schema file: "+str(e))


# Get the single event log and check each of them
def validate_by_schema(event_str: str, schema: str):
    event_list = json.loads(event_str)
    params_json = json.loads(schema)
    items = params_json.items()
    # record the number of line which the system is checking
    line_count = 1
    for event_json in event_list:
        for key, value in items:
            # schema item with a list of cols
            if str(value).find('[') != -1:
                for name in list(value):
                    res = validate(name, event_json, key, line_count)
                    if not res['isSuccess']:
                        return res
            # schema item with a single col
            else:
                res = validate(value, event_json, key, line_count)
                if not res['isSuccess']:
                    return res
        line_count += 1
    message = 'structure correct :)'
    return response(True, message)


# main validate function
# @name: col name
# @event_json: single event log json
# @key: schema information containing the type of col
def validate(name, event_json, key, index):
    # check if the event log has the attribute
    if str(name) not in event_json:
        message = '[' + str(index) + '] without the column for \"' + name + '\"'
        return response(False, message)

    # check the digital cols
    if str(key).lower().find('num') != -1 or str(key).lower().find('id') != -1 or str(key).lower().find('ignore') != -1:
        if event_json[name] is not None and event_json[name] != "" and \
                str(type(event_json[name])).split('\'')[1] not in ['int', 'float', 'double']:
            message = '\"' + str(name) + '\" should be a number'
            return response(False, message)

    # check the timestamp cols
    if str(key).lower().find('timestamp') != -1:
        if event_json[name] is not None:
            res = check_timestamp(event_json[name])
            if not res["isSuccess"]:
                message = '[' + str(index) + '] \"' + str(name) + '\": ' + res["msg"]
                return response(False, message)

    # check the bool cols
    if str(key).lower().find('future_values') != -1:
        if event_json[name] is not None and \
                'bool' not in str(type(event_json[name])):
            message = '\"' + str(name) + '\" should be a boolean'
            return response(False, message)
    return response(True, '[' + str(index) + '] line correct')


# check the timestamp
def check_timestamp(timestamp: str):
    try:
        pd.to_datetime(timestamp)
        return response(True, "correct")
    except Exception as e:
        return response(False, str(e))


# generate a response
def response(status: bool, msg: str):
    return {'isSuccess': status, 'msg': msg}


# check the config files
def validate_config(config_path: str):
    try:
        config_str = open(config_path).read()
        config_json = json.loads(config_str)
        target_key = list(config_json.keys())[0]
        if len(config_json) > 3:
            return response(False, "config file should only have two or three attributes")
        if target_key not in ["label", "remtime"]:
            return response(False, target_key + " is not a parameter of config json")
        ui_data_key = list(config_json.keys())[1]
        if ui_data_key != "ui_data":
            return response(False, target_key + " is not a parameter of config json")
        for n, n_v in config_json[ui_data_key].items():
            if n not in ["log_file", "job_owner", "start_time"]:
                return response(False, n + " is not a parameter of ui data")
        evaluation_key = list(config_json.keys())[2]
        if len(config_json) == 3 and evaluation_key != "evaluation":
            return response(False, evaluation_key + " is not a parameter of config json")
        bucket = config_json[target_key]
        if len(bucket) != 1:
            return response(False, target_key + " should only have one attribute")
        bucketing_type = list(bucket.keys())[0]
        if bucketing_type not in ["zero", "cluster", "state", "prefix"]:
            return response(False, bucketing_type + " is not a parameter of a bucket")
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
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_features"]:
                    return response(False, p + " is not a parameter of " + learner_type)
        elif learner_type == "gbm":
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_features", "learning_rate"]:
                    return response(False, p + " is not a parameter of " + learner_type)
        elif learner_type == "dt":
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "max_features", "max_depth"]:
                    return response(False, p + " is not a parameter of " + learner_type)
        elif learner_type == "xgb":
            for p, p_v in l_v.items():
                if p not in ["n_clusters", "n_estimators", "max_depth", "learning_rate", "colsample_bytree", "subsample"]:
                    return response(False, p + " is not a parameter of " + learner_type)
        else:
            return response(False, learner_type + " is not a parameter of learner")
        return response(True, "config file is correct")
    except Exception as e:
        return response(False, str(e))
