import os, sys
import uuid
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
import services.file_handler as fh
from uuid import uuid4,UUID
from fastapi import UploadFile, File

taskID = '13c43b4c-2417-49af-942b-e12e130db221'



#--------------------------convertion functions-------------------------------------
def test_parquet2Csv():
  expect = 'Parquet file not found'
  actual = fh.parquet2Csv('','') 
  assert expect == actual

  expect = True
  fh.parquet2Csv('test_files/test-event-log.parquet','test_files/test-event-log.csv')
  actual = os.path.exists('test_files/test-event-log.csv')
  assert expect == actual

def test_parquetGenerateCsv():
  parquet_address = '../predict_files/13c43b4c-2417-49af-942b-e12e130db221/test-event-log.parquet'
  csv_address = '../predict_files/13c43b4c-2417-49af-942b-e12e130db221/test-event-log.csv'

  expect = 'Parquet file not found'
  actual = fh.parquetGenerateCsv("")
  assert expect == actual

  expect = True
  fh.parquetGenerateCsv(parquet_address)
  actual = os.path.exists(csv_address)
  assert expect == actual

  fh.csv2Parquet(csv_address, parquet_address)
  fh.removeFile(csv_address)

#----------------------------file loading functions----------------------------------------

def test_pickle():
  expect = 'pickle not exist'
  actual = fh.pickleLoadingAsDict('')
  assert expect == actual 

  expect = dict({'one': 1, 'two': {2.1: ['a', 'b']}})
  actual = fh.pickleLoadingAsDict('test_files/test.pickle')
  assert expect == actual


def test_loadPredictRoot():

  expect = 'Root not exist'
  actual = fh.loadPredictRoot('','')
  assert expect == actual

  expect = '../predict_files\\13c43b4c-2417-49af-942b-e12e130db221'
  actual = fh.loadPredictRoot(taskID,'../')
  assert expect == actual

#-----------------------------------Eventlog functions----------------------------------------------

def test_savePredictEventlog():
  new_taskID = str(uuid4())

  file = UploadFile('test.pickle',open('test_files/test.pickle','rb'))
  expect = 'Eventlog File not accepted'
  actual = fh.savePredictEventlog(new_taskID, file,'../')
  assert expect == actual

  file = UploadFile('test-event-log.csv',open('test_files/test-event-log.csv','rb'))
  expect = '../' + os.path.join('predict_files',new_taskID,'test-event-log.csv')
  actual = fh.savePredictEventlog(new_taskID, file,'../')
  assert expect == actual

  file = UploadFile('test-event-log.parquet',open('test_files/test-event-log.parquet','rb'))
  expect = '../' + os.path.join('predict_files',taskID,'test-event-log.parquet')
  actual = fh.savePredictEventlog(taskID, file,'../')
  assert expect == actual

  fh.removePredictTaskFile(new_taskID,'../')


def test_loadPredictEventLogAddress():
  non_exist_taskID = str(uuid4())
  file_name = ''
  expect = 'Eventlog not found'
  actual = fh.loadPredictEventLogAddress(non_exist_taskID, file_name, '../')
  assert expect == actual

  file_name = 'test-event-log.parquet'
  expect = '../' + os.path.join('predict_files',taskID,'test-event-log.parquet')
  actual = fh.loadPredictEventLogAddress(taskID, file_name, '../')
  assert expect == actual


#---------------------------------Pickle functions---------------------------------------------
def test_savePredictor():
  new_taskID = str(uuid4())

  file = []
  expect = 'No predictor'
  actual = fh.savePredictor(new_taskID, file,'../')
  assert expect == actual

  file = [UploadFile('test-event-log.parquet',open('test_files/test-event-log.parquet','rb'))]
  expect = 'Pickle file not accept'
  actual = fh.savePredictor(new_taskID, file,'../')
  assert expect == actual

  file = [UploadFile('test-label-predictor.pkl',open('test_files/test-label-predictor.pkl','rb'))]
  expect = 'Pickles saved'
  actual = fh.savePredictor(taskID, file,'../')
  assert expect == actual

def test_loadPredictorAddress():
  non_exist_taskID = str(uuid4())

  expect = 'Predictor does not exists'
  actual = fh.loadPredictorAddress(non_exist_taskID)
  assert expect == actual

  expect = '../' + os.path.join('predict_files',taskID,'predictor')
  actual = fh.loadPredictorAddress(taskID,'../')
  assert expect == actual

#---------------------------------Schema functions---------------------------------------------
def test_savePredictSchema():
  new_taskID = str(uuid4())

  file = UploadFile('test.pickle',open('test_files/test.pickle','rb'))
  expect = 'Schema file not accept'
  actual = fh.savePredictSchema(new_taskID, file,'../')
  assert expect == actual


  file = UploadFile('test-schema.json',open('test_files/test-schema.json','rb'))
  expect = '../' + os.path.join('predict_files',taskID,'test-schema.json')
  actual = fh.savePredictSchema(taskID, file,'../')
  assert expect == actual

def test_loadPredictSchema():
  non_exist_taskID = str(uuid4())

  file_name = ''
  expect = 'Schema not found'
  actual = fh.loadPredictSchemaAddress(non_exist_taskID, file_name, '../')
  assert expect == actual

  file_name = 'test-schema.json'
  expect = '../' + os.path.join('predict_files',taskID,'test-schema.json')
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
  expect = '../' + os.path.join('predict_files',taskID, taskID + '-results.csv')
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
  actual = fh.fileExistanceCheck(['test_files/test-event-log.csv'])
  assert expect == actual

def test_csvCheck():
  expect = False
  actual = fh.csvCheck('')
  assert expect == actual

  expect = True
  actual = fh.csvCheck('test_files/test-event-log.csv')
  assert expect == actual

def test_pickleCheck():
  expect = False
  actual = fh.pickleCheck('')
  assert expect == actual

  expect = True
  actual = fh.pickleCheck('test_files/test.pickle')
  assert expect == actual

def test_schema():
  expect = False
  actual = fh.schemaCheck('')
  assert expect == actual

  expect = True
  actual = fh.schemaCheck('test_files/test-schema.json')
  assert expect == actual

def test_parquet():
  expect = False
  actual = fh.parquetCheck('')
  assert expect == actual

  expect = True
  actual = fh.parquetCheck('test_files/test-event-log.parquet')
  assert expect == actual