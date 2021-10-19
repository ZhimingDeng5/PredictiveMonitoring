import os, sys
import uuid
import commons.file_handler as fh
from uuid import uuid4, UUID
from fastapi import UploadFile, File
sys.path.insert(1, '../')

taskID = '13c43b4c-2417-49af-942b-e12e130db221'

task_root = os.path.join('../','predict_files',taskID)

csv_address = '../../../DataSamples/bpi/test-event-log.csv'
parquet_address = '../../../DataSamples/bpi/test-event-log.parquet'
pickle_address = '../../../DataSamples/bpi/predictors/test-label-predictor.pkl'
schema_address = '../../../DataSamples/bpi/test-schema.json'


test_csv_address = 'test_files/test-event-log.csv'
test_parquet_address = 'test_files/test-event-log.parquet'
test_pickle_address = 'test_files/test.pickle'

csv_file = UploadFile('test-event-log.csv',open(csv_address,'rb'))
parquet_file = UploadFile('test-event-log.parquet',open(parquet_address,'rb'))
pickle_file = [UploadFile('test-label-predictor.pkl',open(pickle_address,'rb'))]
schema_file = UploadFile('test-schema.json',open(schema_address,'rb'))



fh.savePredictEventlog(taskID,csv_file,'../')
fh.savePredictEventlog(taskID,parquet_file,'../')
fh.savePredictor(taskID, pickle_file,'../')
fh.savePredictSchema(taskID,schema_file,'../')


#--------------------------convertion functions-------------------------------------
def test_parquet2Csv():
  expect = 'Parquet file not found'
  actual = fh.parquet2Csv('','') 
  assert expect == actual

  expect = True
  fh.parquet2Csv(parquet_address,test_csv_address)
  actual = os.path.exists(test_csv_address)
  assert expect == actual

def test_parquetGenerateCsv():
  fh.csv2Parquet(csv_address,test_parquet_address)

  expect = 'Parquet file not found'
  actual = fh.parquetGenerateCsv('')
  assert expect == actual

  expect = True
  fh.parquetGenerateCsv(test_parquet_address)
  actual = os.path.exists(test_csv_address)
  assert expect == actual


#----------------------------file loading functions----------------------------------------

def test_pickle():
  expect = 'pickle not exist'
  actual = fh.pickleLoadingAsDict('')
  assert expect == actual 

  expect = dict({'one': 1, 'two': {2.1: ['a', 'b']}})
  actual = fh.pickleLoadingAsDict(test_pickle_address)
  assert expect == actual


def test_loadPredictRoot():

  expect = 'Root not exist'
  actual = fh.loadPredictRoot('','')
  assert expect == actual

  expect = task_root
  actual = fh.loadPredictRoot(taskID,'../')
  assert expect == actual

#-----------------------------------Eventlog functions----------------------------------------------
def test_savePredictEventlog():
  new_taskID = str(uuid4())

  expect = 'Eventlog File not accepted'
  actual = fh.savePredictEventlog(new_taskID, schema_file,'../')
  assert expect == actual

  expect = os.path.join('../','predict_files',new_taskID,'test-event-log.csv')
  actual = fh.savePredictEventlog(new_taskID, csv_file,'../')
  assert expect == actual

  expect = os.path.join('../','predict_files',taskID,'test-event-log.parquet')
  actual = fh.savePredictEventlog(taskID, parquet_file,'../')
  assert expect == actual

  fh.removePredictTaskFile(new_taskID,'../')


def test_loadPredictEventLogAddress():
  non_exist_taskID = str(uuid4())

  file_name = ''
  expect = 'Eventlog not found'
  actual = fh.loadPredictEventLogAddress(non_exist_taskID, file_name, '../')
  assert expect == actual

  file_name = 'test-event-log.parquet'
  expect = os.path.join('../', 'predict_files',taskID,'test-event-log.parquet')
  actual = fh.loadPredictEventLogAddress(taskID, file_name, '../')
  assert expect == actual


#---------------------------------Pickle functions---------------------------------------------
def test_savePredictor():
  non_exist_taskID = str(uuid4())

  file = []
  expect = 'No predictor'
  actual = fh.savePredictor(non_exist_taskID, file,'../')
  assert expect == actual

  expect = 'Pickle file not accept'
  actual = fh.savePredictor(non_exist_taskID, [parquet_file],'../')
  assert expect == actual

  expect = 'Pickles saved'
  actual = fh.savePredictor(taskID, pickle_file,'../')
  assert expect == actual

def test_loadPredictorAddress():
  non_exist_taskID = str(uuid4())

  expect = 'Predictor does not exists'
  actual = fh.loadPredictorAddress(non_exist_taskID)
  assert expect == actual

  expect = os.path.join(task_root,'predictor')
  actual = fh.loadPredictorAddress(taskID,'../')
  assert expect == actual

#---------------------------------Schema functions---------------------------------------------
def test_savePredictSchema():
  new_taskID = str(uuid4())

  expect = 'Schema file not accept'
  actual = fh.savePredictSchema(new_taskID, csv_file,'../')
  assert expect == actual

  expect = os.path.join('../','predict_files',taskID,'test-schema.json')
  actual = fh.savePredictSchema(taskID, schema_file,'../')
  assert expect == actual

def test_loadPredictSchema():
  non_exist_taskID = str(uuid4())

  file_name = ''
  expect = 'Schema not found'
  actual = fh.loadPredictSchemaAddress(non_exist_taskID, file_name, '../')
  assert expect == actual

  file_name = 'test-schema.json'
  expect = os.path.join('../','predict_files',taskID,'test-schema.json')
  actual = fh.loadPredictSchemaAddress(taskID, file_name, '../')
  assert expect == actual


#------------------------------Result functions---------------------------------------------------
def test_loadPredictResult():
  non_exist_taskID = str(uuid4())
  expect = 'Task not exist'
  actual = fh.loadPredictResult(non_exist_taskID,'../')
  assert expect == actual
  
  file = UploadFile(taskID+'-results.csv',open('test_files/test-event-log.csv','rb'))
  fh.savePredictEventlog(taskID,file,'../')
  expect = os.path.join('../','predict_files',taskID, taskID + '-results.csv')
  actual = fh.loadPredictResult(taskID,'../')
  assert expect == actual

  fh.removeFile(actual)
  expect = 'Result not found'
  actual = fh.loadPredictResult(taskID,'../')
  assert expect == actual


#------------------------------File checking functions---------------------------------------------------
def test_fileExistanceCheck():
  expect = False
  actual = fh.fileExistanceCheck([''])
  assert expect == actual

  expect = True
  actual = fh.fileExistanceCheck([csv_address])
  assert expect == actual

def test_csvCheck():
  expect = False
  actual = fh.csvCheck('')
  assert expect == actual

  expect = True
  actual = fh.csvCheck(csv_address)
  assert expect == actual

def test_pickleCheck():
  expect = False
  actual = fh.pickleCheck('')
  assert expect == actual

  expect = True
  actual = fh.pickleCheck(pickle_address)
  assert expect == actual

def test_json():
  expect = False
  actual = fh.jsonCheck('')
  assert expect == actual

  expect = True
  actual = fh.jsonCheck(schema_address)
  assert expect == actual

def test_parquet():
  expect = False
  actual = fh.parquetCheck('')
  assert expect == actual

  expect = True
  actual = fh.parquetCheck(parquet_address)
  assert expect == actual


#--------------------------------Delete functions-------------------------------------------------
def test_removePredictTaskFile():
  expect = 'Task '+''+' not found'
  actual = fh.removePredictTaskFile('')
  assert expect == actual

  expect = 'Task ' + taskID + ' has been deleted'
  actual = fh.removePredictTaskFile(taskID,'../')
  assert expect == actual

def test_removeFile():
  expect = 'File not found'
  actual = fh.removeFile('')
  assert expect == actual

  expect = 'File test_files/test-event-log.csv has been deleted'
  actual = fh.removeFile('test_files/test-event-log.csv')
  assert expect == actual

  fh.removeFile('test_files/test-event-log.parquet')

#--------------------------------Common functions-------------------------------------------------
def test_saveFile():
  expect = os.path.join('../', 'predict_files', taskID,'test-event-log.parquet')
  actual = fh.saveFile(task_root, parquet_file)
  assert expect == actual

  fh.removePredictTaskFile(taskID,'../')
