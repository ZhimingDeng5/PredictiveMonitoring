from file_handler import *
import json


# used for validating the event log (csv) file by schema
def validate_csv_by_schema(csv_path: str, schema: str):
    try:
        cf = pd.read_csv(csv_path, index_col=False)
        s = cf.to_json(orient='records')
        return validate_by_schema(s, schema)
    except Exception:
        return False


# used for validating the event log (json) file by schema
def validate_json_by_schema(json_path: str, schema: str):
    try:
        jf = pd.read_json(json_path)
        s = jf.to_json(orient='records')
        return validate_by_schema(s, schema)
    except Exception:
        return False


# Get the single event log and check each of them
def validate_by_schema(event_str: str, schema: str):
    event_list = json.loads(event_str)
    params_json = json.loads(schema)
    items = params_json.items()
    for event_json in event_list:
        for key, value in items:
            # schema item with a list of cols
            if str(value).find('[') != -1:
                for name in list(value):
                    if not validate(name, event_json, key):
                        return False
            # schema item with a single col
            else:
                if not validate(value, event_json, key):
                    return False
    return True


# main validate function
# @name: col name
# @event_json: single event log json
# @key: schema information containing the type of col
def validate(name, event_json, key):
    # check if the event log has the attribute
    if str(name) not in event_json:
        return False

    # check the digital cols
    if str(key).find('num') != -1 or str(key).find('id') != -1:
        if event_json[name] is not None and event_json[name] != "" and \
                str(type(event_json[name])).split('\'')[1] not in ['int', 'float', 'double']:
            return False

    # check the timestamp cols
    if str(key).find('timestamp') != -1:
        if event_json[name] is not None:
            if not check_timestamp(event_json[name]):
                return False

    # check the bool cols
    if str(key).find('future_values') != -1:
        if event_json[name] is not None and \
                'bool' not in str(type(event_json[name])):
            return False
    return True


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


# For test
# sc = open("../../../DataSamples/bpi17_sample_schema.json").read()
# cs = "../../../DataSamples/bpi17_sample.csv"
# print(validate_csv_by_schema(cs, sc))
# ev = "../../../DataSamples/bpi17_sample_event.json"
# print(validate_json_by_schema(ev, sc))
