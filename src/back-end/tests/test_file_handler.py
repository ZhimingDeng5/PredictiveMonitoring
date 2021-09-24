import os, sys
import uuid
sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
import services.file_handler as fh
from uuid import uuid4,UUID

#--------------------------convertion functions-------------------------------------
def test_parquet2Csv():
  fh.parquet2Csv('','')
  assert fh.fileExistanceCheck(['']) == False
  fh.parquet2Csv('test_files/test-event-log.parquet','test_files/test-event-log.csv')
  assert fh.fileExistanceCheck(['test_files/test-event-log.csv']) ==True
  fh.removeFile('test_files/test-event-log.csv')

def test_parquetGenerateCsv():
  taskID = '8afe2500-d68d-4e6f-b03f-dcaaf3419fc4'
  fh.parquetGenerateCsv(taskID, 'test-event-log.csv',fh.loadPredictEventLogAddress(taskID,'test-event-log.parquet'))
  assert fh.fileExistanceCheck(fh.loadPredictEventLogAddress(taskID,'test-event-log.parquet')) ==True

print(fh.loadPredictEventLogAddress('8afe2500-d68d-4e6f-b03f-dcaaf3419fc4','test-event-log.parquet'))