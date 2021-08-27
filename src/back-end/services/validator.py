from file_handler import *
import json
import pickle


# used for validating the event log (csv) file by schema
def validate_csv_in_path(csv_path: str, schema_path: str):
    try:
        cf = pd.read_csv(csv_path, index_col=False)
        s = cf.to_json(orient='records')
        schema = open(schema_path).read()
        return validate_by_schema(s, schema)
    except Exception:
        return response(False, "Wrong type for csv file or schema file")


# used for validating the event log (json) file by schema
def validate_json_in_path(json_path: str, schema_path: str):
    try:
        jf = pd.read_json(json_path)
        s = jf.to_json(orient='records')
        schema = open(schema_path).read()
        return validate_by_schema(s, schema)
    except Exception:
        return response(False, "Wrong type for json file or schema file")


# used for validating the event log (csv) file by schema
def validate_csv_in_file(csv: UploadFile, schema: UploadFile):
    try:
        cf = pd.read_csv(csv.file, index_col=False)
        s = cf.to_json(orient='records')
        _schema = pd.read_json(schema.file)
        return validate_by_schema(s, _schema)
    except Exception:
        return response(False, "Wrong type for csv file or schema file")


# used for validating the event log (json) file by schema
def validate_json_in_file(json_file: UploadFile, schema: UploadFile):
    try:
        jf = pd.read_json(json_file.file)
        s = jf.to_json(orient='records')
        _schema = pd.read_json(schema.file)
        return validate_by_schema(s, _schema)
    except Exception:
        return response(False, "Wrong type for json file or schema file")


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
    if str(key).find('num') != -1 or str(key).find('id') != -1 or str(key).find('ignore') != -1:
        if event_json[name] is not None and event_json[name] != "" and \
                str(type(event_json[name])).split('\'')[1] not in ['int', 'float', 'double']:
            message = '\"' + str(name) + '\" should be a number'
            return response(False, message)

    # check the timestamp cols
    if str(key).find('timestamp') != -1:
        if event_json[name] is not None:
            if not check_timestamp(event_json[name]):
                message = '[' + str(index) + '] \"' + str(name) + '\" should be a timestamp'
                return response(False, message)

    # check the bool cols
    if str(key).find('future_values') != -1:
        if event_json[name] is not None and \
                'bool' not in str(type(event_json[name])):
            message = '\"' + str(name) + '\" should be a boolean'
            return response(False, message)
    return response(True, '['+str(index)+'] line correct')


# check the timestamp
def check_timestamp(cal: str):
    timestamp = cal.split(' ')
    if len(timestamp) != 2:
        return False
    date = timestamp[0]
    time = timestamp[1]
    return check_date_time(date, '/') and check_date_time(time, ':')


# check the date and time
def check_date_time(d: str, s: str):
    dd = d.split(s)
    if len(dd) != 3:
        return False
    for n in dd:
        if not n.isdigit():
            return False
    return True


# generate a response
def response(status: bool, msg: str):
    return {'isSuccess': status, 'msg': msg}