from uuid import uuid4, UUID
from fastapi import UploadFile, File
import commons.file_handler as fh
import uuid
import os
import sys
sys.path.insert(1, '../')


taskID = '13c43b4c-2417-49af-942b-e12e130db221'

task_root = os.path.join('../', 'training_files', taskID)

csv_address = '../../DataSamples/bpi/test-event-log.csv'
parquet_address = '../../DataSamples/bpi/test-event-log.parquet'
schema_address = '../../DataSamples/bpi/test-schema.json'
config_address = '../../DataSamples/bpi/myconfig_label.json'

test_csv_address = 'test_files/test-event-log.csv'
test_parquet_address = 'test_files/test-event-log.parquet'

csv_file = UploadFile('test-event-log.csv', open(csv_address, 'rb'))
parquet_file = UploadFile('test-event-log.parquet',
                          open(parquet_address, 'rb'))
schema_file = UploadFile('test-schema.json', open(schema_address, 'rb'))
config_file = UploadFile('myconfig_label.json', open(config_address, 'rb'))


fh.saveTrainingEventlog(taskID, csv_file, '../')
fh.saveTrainingEventlog(taskID, parquet_file, '../')
fh.saveTrainingSchema(taskID, schema_file, '../')
fh.saveConfig(taskID, config_file, '../')


# ----------------------------file loading functions----------------------
def test_loadTrainingRoot():

    expect = 'Root not exist'
    actual = fh.loadTrainingRoot('', '')
    assert expect == actual

    expect = task_root
    actual = fh.loadTrainingRoot(taskID, '../')
    assert expect == actual


# -----------------------------------Eventlog functions-------------------
def test_saveTrainingEventlog():
    new_taskID = str(uuid4())

    expect = 'Eventlog File not accepted'
    actual = fh.saveTrainingEventlog(new_taskID, schema_file, '../')
    assert expect == actual

    expect = os.path.join('../', 'training_files',
                          new_taskID, 'test-event-log.csv')
    actual = fh.saveTrainingEventlog(new_taskID, csv_file, '../')
    assert expect == actual

    expect = os.path.join('../', 'training_files',
                          taskID, 'test-event-log.parquet')
    actual = fh.saveTrainingEventlog(taskID, parquet_file, '../')
    assert expect == actual

    fh.removeTrainingTaskFile(new_taskID, '../')


def test_loadTrainingEventLogAddress():
    non_exist_taskID = str(uuid4())

    file_name = ''
    expect = 'Eventlog not found'
    actual = fh.loadTrainingEventLogAddress(non_exist_taskID, file_name, '../')
    assert expect == actual

    file_name = 'test-event-log.parquet'
    expect = os.path.join('../', 'training_files',
                          taskID, 'test-event-log.parquet')
    actual = fh.loadTrainingEventLogAddress(taskID, file_name, '../')
    assert expect == actual


# ---------------------------------Schema functions-----------------------
def test_saveTrainingSchema():
    new_taskID = str(uuid4())

    expect = 'Schema file not accept'
    actual = fh.saveTrainingSchema(new_taskID, csv_file, '../')
    assert expect == actual

    expect = os.path.join('../', 'training_files', taskID, 'test-schema.json')
    actual = fh.saveTrainingSchema(taskID, schema_file, '../')
    assert expect == actual


def test_loadTrainingSchema():
    non_exist_taskID = str(uuid4())

    file_name = ''
    expect = 'Schema not found'
    actual = fh.loadTrainingSchemaAddress(non_exist_taskID, file_name, '../')
    assert expect == actual

    file_name = 'test-schema.json'
    expect = os.path.join('../', 'training_files', taskID, 'test-schema.json')
    actual = fh.loadTrainingSchemaAddress(taskID, file_name, '../')
    assert expect == actual


# ------------------------------Config functions--------------------------
def test_saveConfig():
    new_taskID = str(uuid4())

    expect = 'Config file not accept'
    actual = fh.saveConfig(new_taskID, csv_file, '../')
    assert expect == actual

    expect = os.path.join('../', 'training_files',
                          taskID, 'myconfig_label.json')
    actual = fh.saveConfig(taskID, config_file, '../')
    assert expect == actual


def test_loadConfig():
    non_exist_taskID = str(uuid4())

    file_name = ''
    expect = 'Config not found'
    actual = fh.loadConfigAddress(non_exist_taskID, file_name, '../')
    assert expect == actual

    file_name = 'myconfig_label.json'
    expect = os.path.join('../', 'training_files',
                          taskID, 'myconfig_label.json')
    actual = fh.loadConfigAddress(taskID, file_name, '../')
    assert expect == actual


# ------------------------------Result functions--------------------------


# -------------------------------zip functions----------------------------
def test_zipFile():
    not_exist_id = str(uuid4())

    expect = False
    actual = fh.zipFile(not_exist_id, True, '../')
    assert expect == actual

    expect = True
    actual = fh.zipFile(taskID, False, '../')
    assert expect == actual


def test_loadZip():
    not_exist_id = str(uuid4())

    expect = 'zip result not found'
    actual = fh.loadZip(not_exist_id, '../')
    assert expect == actual

    expect = os.path.join('../', 'training_files',
                          taskID, taskID + '-results.zip')
    actual = fh.loadZip(taskID, '../')
    assert expect == actual

    fh.removeTrainingTaskFile(taskID, '../')
