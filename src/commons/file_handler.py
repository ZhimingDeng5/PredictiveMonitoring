import os
import json

from typing import List

from fastapi.datastructures import UploadFile
import pandas as pd
import pickle
import base64

import shutil
import zipfile


predict_root = 'predict_files'
training_root = 'training_files'
predictor = 'predictor'

# -------------------------conversion functions------------------------------------


# csv -> parquet
def csv2Parquet(input_path: str, output_path: str):
    cf = pd.read_csv(input_path, index_col=False)
    cf.to_parquet(output_path)


# parquet -> csv
def parquet2Csv(input_path: str, output_path: str):
    pf = pd.read_parquet(input_path)
    pf.to_csv(output_path, index = False)


# csv -> json format
def csv2Json(input_path: str, output_path: str):
    cf = pd.read_csv(input_path)
    cf.to_json(output_path, orient='records')


# json file -> csv
def json2Csv(input_path: str, output_path: str):
    jf = pd.read_json(input_path)
    jf.to_csv(output_path, index=False)


# csv -> pickle
def csv2Pickle(input_path: str, output_path: str):
    cf = pd.read_csv(input_path)
    cf.to_pickle(output_path)


# pickle -> csv
def pickle2Csv(input_path: str, output_path: str):
    pf = pd.read_pickle(input_path)
    pf.to_csv(output_path)


def parquetGenerateCsv(uuid: str, file_name: str, input_address: str):
    filename, extension = os.path.splitext(file_name)
    new_log = loadPredictEventLogAddress(uuid, filename) + '.csv'
    print('Parquet->CSV start...')
    parquet2Csv(input_address, new_log)
    print('Parquet->CSV finished...Remove Parquet...')
    removeFile(input_address)
    return new_log


# ---------------------------file loading functions-------------------------------
# loading CSV file into String format
def csvLoadingAsString(input_path: str):
    cf = pd.read_csv(input_path, index_col=False)
    s = cf.to_json()
    return s


# loading CSV file into json dict
def csvLoadingAsDict(input_path: str):
    s = csvLoadingAsString(input_path)
    jd = json.loads(s)
    return jd


def csvLoadingHead(input_path: str):
    ch = pd.read_csv(input_path)
    return ch.head()


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
    with open(pickle_path, 'rb') as pf:
        _pd = pickle.load(pf)
    return _pd


# load root address
def loadPredictRoot(uuid: str,  volume_address=''):

    address = os.path.join(volume_address, predict_root, uuid)
    return address


def loadTrainingRoot(uuid: str,  volume_address=''):
    address = os.path.join(volume_address, training_root, uuid)

    return address

# ----------------------------------Eventlog functions-------------------------------
# save predictive monitor csv file
# Volume address logic needs to be solved later
def savePredictEventlog(uuid: str, file: UploadFile, volume_address = ''):
    root_address = os.path.join(volume_address, predict_root, uuid)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    with open(os.path.join(root_address, file.filename), 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


# load EventLog address
def loadPredictEventLogAddress(uuid: str, file_name: str, volume_address=''):
    root_address = os.path.join(volume_address, predict_root, uuid, file_name)

    return root_address


# save training Eventlog
def saveTrainingEventlog(uuid: str, file: UploadFile, volume_address=''):
    root_address = os.path.join(volume_address, training_root, uuid)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    with open(os.path.join(root_address, file.filename), 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


# load training event log address
def loadTrainingEventLogAddress(uuid: str, file_name: str, volume_address=''):
    root_address = os.path.join(volume_address, training_root, uuid, file_name)

    return root_address


# --------------------------------Pickle functions---------------------------------------------
# save pickle dict as pickle file
def savePredictor(uuid: str, files: List[UploadFile], volume_address=''):
    root_address = os.path.join(volume_address, predict_root, uuid, predictor)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    for pfile in files:
        with open(os.path.join(root_address, pfile.filename), 'wb') as buffer:
            shutil.copyfileobj(pfile.file, buffer)


# load pickle file address by uuid and name
def loadPredictorAddress(uuid: str, volume_address=''):
    root_address = os.path.join(volume_address, predict_root, uuid, predictor)

    return root_address


# -------------------------------Schema functions-------------------------------------------------
# save Schema dict as pickle file
def savePredictSchema(uuid: str, file: UploadFile, volume_address=''):
    root_address = os.path.join(volume_address, predict_root, uuid)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    with open(os.path.join(root_address, file.filename), 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


def saveTrainingSchema(uuid: str, file: UploadFile, volume_address=''):
    root_address = os.path.join(volume_address, training_root, uuid)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    with open(os.path.join(root_address,file.filename), 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


# load pickle file address by uuid and name
def loadPredictSchemaAddress(uuid: str, file_name: str, volume_address=''):

    root_address = os.path.join(volume_address, predict_root, uuid, file_name)
    return root_address


def loadTrainingSchemaAddress(uuid: str, file_name: str, volume_address=''):

    root_address = os.path.join(volume_address, training_root, uuid, file_name)
    return root_address


# -----------------------------Config functions---------------------------------------------------
def saveConfig(uuid: str, file: UploadFile, volume_address=''):
    root_address = os.path.join(volume_address, training_root, uuid)
    folder = os.path.exists(root_address)

    if not folder:
        os.makedirs(root_address)

    with open(os.path.join(root_address, file.filename), 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)


# load EventLog address
def loadConfigAddress(uuid: str, file_name: str, volume_address=''):
    root_address = os.path.join(volume_address, training_root, uuid, file_name)

    return root_address


# -----------------------------Result functions---------------------------------------------------
def loadPredictResult(uuid: str, volume_address=''):

    root_address = os.path.join(volume_address, predict_root, uuid)
    allFile = os.listdir(root_address)

    for file in allFile:
        if file == uuid + '-results.csv':
            return os.path.join(root_address, file)


def loadTrainingResult(uuid: str, volume_address=''):

    root_address = os.path.join(volume_address, training_root, uuid)
    allFile = os.listdir(root_address)

    for file in allFile:
        if file == uuid + '-results.zip':
            return os.path.join(root_address, file)


# -----------------------------File checking functions---------------------------------------------------
# check file existence
def fileExistenceCheck(files: List):
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
def schemaCheck(file: str):
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


# check config file in json format
def configCheck(file: str):
    filename, extension = os.path.splitext(file)
  
    if extension == '.json':
        return True
    else:
        return False


# ------------------------------zip functions-----------------------------------------------------
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
def loadZip(uuid: str, volume_address=''):
    zip_address = os.path.join(volume_address, training_root, uuid)+'.zip'

    return zip_address


# -------------------------------Delete functions-------------------------------------------------
def removePredictTaskFile(uuid: str, volume_address=''):
    rm_pass = os.path.join(volume_address, predict_root, uuid)
    shutil.rmtree(rm_pass, onerror=lambda func, path, excinfo: print(excinfo))


def removeTrainingTaskFile(uuid: str, volume_address=''):
    rm_pass = os.path.join(volume_address, training_root, uuid)
    shutil.rmtree(rm_pass, onerror=lambda func, path, excinfo: print(excinfo))


def removeFile(path: str):
    try:
        os.remove(path)
    except OSError as err:
        print(err)


# -----------------------------serializing functions---------------------------------------------------
def baseDecode(base:str):
    return base64.decode(base)


## Docker volume test ##

# docker build -t python-project .
# docker run -it -v abc:/Predictive python-project (volume 'abc' would be created, root dir is /Predictive)
