import os
import json
from typing import List
from fastapi.datastructures import UploadFile
import pandas as pd
import pickle
import shutil
import zipfile

predict_root = 'predict_files'
training_root = 'training_files'
predictor = 'predictor'


# --------------------------conversion functions--------------------------
# csv -> parquet
def csv2Parquet(input_path: str, output_path: str):
    if not fileExistanceCheck([input_path]):
        print('CSV file not found')
        return 'CSV file not found'
    cf = pd.read_csv(input_path, index_col=False)
    cf.to_parquet(output_path)


# parquet -> csv
def parquet2Csv(input_path: str, output_path: str):
    if not fileExistanceCheck([input_path]):
        print('Parquet file not found')
        return 'Parquet file not found'
    pf = pd.read_parquet(input_path)
    pf.to_csv(output_path, index=False)


# csv -> json format
def csv2Json(input_path: str, output_path: str):
    if not fileExistanceCheck([input_path]):
        print('CSV file not found')
        return 'CSV file not found'
    cf = pd.read_csv(input_path)
    cf.to_json(output_path, orient='records')


# json file -> csv
def json2Csv(input_path: str, output_path: str):
    if not fileExistanceCheck([input_path]):
        print('Json file not found')
        return 'Json file not found'
    jf = pd.read_json(input_path)
    jf.to_csv(output_path, index=False)
    print(f'File has been saved at {output_path}')


def parquetGenerateCsv(input_path: str):
    if not fileExistanceCheck([input_path]):
        print('Parquet file not found')
        return 'Parquet file not found'
    file_path, full_name = os.path.split(input_path)
    file_name = full_name.split('.')[0]
    new_log = os.path.join(file_path, file_name + '.csv')
    print('Parquet->CSV start...')
    parquet2Csv(input_path, new_log)
    print('Parquet->CSV finished...')
    return new_log


# ----------------------------file loading functions----------------------
# loading CSV file into String format
def csvLoadingAsString(input_path):
    cf = pd.read_csv(input_path, index_col=False)
    s = cf.to_json()
    return s


# loading CSV file into json dict
def csvLoadingAsDict(input_path: str):
    s = csvLoadingAsString(input_path)
    jd = json.loads(s)
    return jd


# loading json file into string(jsonFormat)(used inside)
def jsonLoadingAsString(js_path: str):
    jf = pd.read_json(js_path)
    s = jf.to_json()
    return s


# loading json file into dict
def jsonLoadingAsDict(js_path: str):
    s = jsonLoadingAsString(js_path)
    jd = json.loads(s)
    return jd


# loading pickle file into dict
def pickleLoadingAsDict(pickle_path: str):
    if not os.path.exists(pickle_path):
        print('pickle not exist')
        return 'pickle not exist'
    with open(pickle_path, 'rb') as pf:
        pd = pickle.load(pf)
    return pd


# load root address
def loadPredictRoot(uuid: str, additional_address=''):
    address = os.path.join(additional_address, predict_root, uuid)

    if not os.path.exists(address):
        print(f'Task {uuid} not exist')
        return 'Root not exist'

    return address


def loadTrainingRoot(uuid: str, additional_address=''):
    address = os.path.join(additional_address, training_root, uuid)

    if not os.path.exists(address):
        print(f'Task {uuid} not exist')
        return 'Root not exist'

    return address


# -----------------------------------Eventlog functions-------------------
# save predictive monitor csv file
def savePredictEventlog(uuid: str, file: UploadFile, additional_address=''):
    if not csvCheck(file.filename) and not parquetCheck(file.filename):
        return 'Eventlog File not accepted'

    root_address = os.path.join(additional_address, predict_root, uuid)

    return saveFile(root_address, file)


# load EventLog address
def loadPredictEventLogAddress(
        uuid: str, file_name: str, additional_address=''):
    root_address = root_address = os.path.join(
        additional_address, predict_root, uuid, file_name)
    if not os.path.exists(root_address):
        return 'Eventlog not found'

    return root_address


# save training Eventlog
def saveTrainingEventlog(uuid: str, file: UploadFile, additional_address=''):
    if not csvCheck(file.filename) and not parquetCheck(file.filename):
        return 'Eventlog File not accepted'

    root_address = os.path.join(additional_address, training_root, uuid)

    return saveFile(root_address, file)


# load training Eventlog address
def loadTrainingEventLogAddress(
        uuid: str, file_name: str, additional_address=''):
    root_address = root_address = os.path.join(
        additional_address, training_root, uuid, file_name)
    if not os.path.exists(root_address):
        return 'Eventlog not found'

    return root_address


# ---------------------------------Pickle functions-----------------------
# save pickle dict as pickle file
def savePredictor(uuid: str, files: List[UploadFile], additional_address=''):
    if files == []:
        return 'No predictor'

    for pfile in files:
        if not pickleCheck(pfile.filename):
            return 'Pickle file not accept'

    for pfile in files:
        root_address = os.path.join(
            additional_address, predict_root, uuid, predictor)
        saveFile(root_address, pfile)

    return 'Pickles saved'


# load pickle file address by uuid and name
def loadPredictorAddress(uuid: str, additional_address=''):
    root_address = root_address = os.path.join(
        additional_address, predict_root, uuid, predictor)

    if not os.path.exists(root_address):
        return 'Predictor does not exists'

    return root_address


# --------------------------------Schema functions------------------------
# save Schema dict as pickle file
def savePredictSchema(uuid: str, file: UploadFile, additional_address=''):
    if not jsonCheck(file.filename):
        return 'Schema file not accept'

    root_address = os.path.join(additional_address, predict_root, uuid)

    return saveFile(root_address, file)


# load pickle file address by uuid and name
def loadPredictSchemaAddress(uuid: str, file_name: str, additional_address=''):
    root_address = root_address = os.path.join(
        additional_address, predict_root, uuid, file_name)
    if not os.path.exists(root_address):
        return 'Schema not found'

    return root_address


def saveTrainingSchema(uuid: str, file: UploadFile, additional_address=''):
    if not jsonCheck(file.filename):
        return 'Schema file not accept'

    root_address = os.path.join(additional_address, training_root, uuid)

    return saveFile(root_address, file)


def loadTrainingSchemaAddress(
        uuid: str, file_name: str, additional_address=''):
    root_address = root_address = os.path.join(
        additional_address, training_root, uuid, file_name)
    if not os.path.exists(root_address):
        return 'Schema not found'

    return root_address


# -----------------------------Config functions---------------------------
def saveConfig(uuid: str, file: UploadFile, additional_address=''):
    if not jsonCheck(file.filename):
        return 'Config file not accept'

    root_address = os.path.join(additional_address, training_root, uuid)

    return saveFile(root_address, file)


# load EventLog address
def loadConfigAddress(uuid: str, file_name: str, additional_address=''):
    root_address = os.path.join(
        additional_address, training_root, uuid, file_name)
    if not os.path.exists(root_address):
        return 'Config not found'

    return root_address


# ------------------------------Result functions--------------------------
def loadPredictResult(uuid: str, additional_address=''):
    root_address = os.path.join(additional_address, predict_root, uuid)
    if not os.path.exists(root_address):
        return 'Task not exist'

    allFile = os.listdir(root_address)

    for file in allFile:
        if file == uuid + '-results.csv':
            return os.path.join(root_address, file)

    return 'Result not found'


def loadTrainingResult(uuid: str, additional_address=''):
    root_address = os.path.join(additional_address, training_root, uuid)
    allFile = os.listdir(root_address)

    for file in allFile:
        if file == uuid + '-results.zip':
            return os.path.join(root_address, file)


# ------------------------------File checking functions-------------------
# check file existance
def fileExistanceCheck(files: List):
    result = True

    for file in files:
        if not os.path.exists(file):
            result = False

    return result


# check the file in csv format
def csvCheck(file: str):
    filename, extension = os.path.splitext(file)

    if extension == '.csv':
        return True
    else:
        return False


# check the  file in pickle format
def pickleCheck(file: str):
    filename, extension = os.path.splitext(file)

    if extension == '.pkl' or extension == '.pickle':
        return True
    else:
        return False


# check schema file in json format
def jsonCheck(file: str):
    filename, extension = os.path.splitext(file)

    if extension == '.json':
        return True
    else:
        return False


# check parquet file
def parquetCheck(file: str):
    filename, extension = os.path.splitext(file)

    if extension == '.parquet':
        return True
    else:
        return False


# ------------------------------zip functions-----------------------------
def zipFile(uuid: str, keep_files: bool = True, volume_address: str = ''):
    startdir = os.path.join(volume_address, training_root, uuid)

    if not os.path.exists(startdir):
        return False

    # z = zipfile.ZipFile(os.path.join(startdir, f"{uuid}-results.zip"), 'w', zipfile.ZIP_DEFLATED)

    zip_contents = []
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            zip_contents.append((os.path.join(dirpath, filename), filename))
            # z.write(os.path.join(dirpath, filename))
    # z.close()

    with zipfile.ZipFile(os.path.join(startdir, f"{uuid}-results.zip"), "w", zipfile.ZIP_DEFLATED) as zipped:
        for abs_filename, filename in zip_contents:
            zipped.write(abs_filename, arcname=filename)
            if not keep_files:
                os.remove(abs_filename)

    # shutil.rmtree(startdir)
    return True


# load zip address by uuid
def loadZip(uuid: str, additional_address=''):
    zip_address = os.path.join(
        additional_address, training_root, uuid, uuid + '-results.zip')

    if not os.path.exists(zip_address):
        return 'zip result not found'

    return zip_address


# --------------------------------Delete functions------------------------
def removePredictTaskFile(uuid: str, additional_address=''):
    rm_pass = os.path.join(additional_address, predict_root, uuid)
    if os.path.exists(rm_pass):
        shutil.rmtree(rm_pass)
        return f'Task {uuid} has been deleted'
    else:
        return f'Task {uuid} not found'


def removeTrainingTaskFile(uuid: str, additional_address=''):
    rm_pass = os.path.join(additional_address, training_root, uuid)
    if os.path.exists(rm_pass):
        shutil.rmtree(rm_pass)
        return f'Task {uuid} has been deleted'
    else:
        return f'Task {uuid} not found'


def removeFile(path: str):
    if os.path.exists(path):
        os.remove(path)
        return f'File {path} has been deleted'
    else:
        return 'File not found'


# ------------------------------common functions--------------------------
def saveFile(address: str, file: UploadFile):
    if not os.path.exists(address):
        os.makedirs(address)

    path = os.path.join(address, file.filename)

    with open(path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
        return path

## Docker volume test ##

# docker build -t python-project .
# docker run -it -v abc:/Predictive python-project (volume 'abc' would be
# created, root dir is /Predictive)
