import os
import json

from typing import List

from fastapi.datastructures import UploadFile
import pandas as pd  
import fastparquet 
import pickle
import base64

import io
import shutil
import zipfile


predict_root = 'predictive_files'



# convertion functions
# csv -> parquet
def csv2Parquet(input_path:str, output_path:str):
  cf = pd.read_csv(input_path, index_col=0)
  cf.to_parquet(output_path)


# parquet -> csv
def parquet2Csv(input_path:str, output_path:str):
  pf = pd.read_parquet(input_path)
  pf.to_csv(output_path)
  cf = pd.read_csv(output_path, index_col=0)


# csv -> json format
def csv2Json(input_path:str, output_path:str):
  cf = pd.read_csv(input_path)
  cf.to_json(output_path, orient='records')


# json file -> csv
def json2Csv(input_path:str, output_path:str):
  jf = pd.read_json(input_path)
  jf.to_csv(output_path, index=False)


# csv -> pickle
def csv2Pickle(input_path:str, output_path:str):
  cf = pd.read_csv(input_path)
  cf.to_pickle(output_path)


# pickle -> csv
def pickle2Csv(input_path:str, output_path:str):
  pf = pd.read_pickle(input_path)
  pf.to_csv(output_path)




#file loading functions:


# loading CSV file into String format
def csvLoadingAsString(input_path):
  cf = pd.read_csv(input_path, index_col= False)
  s = cf.to_json()
  return s

# loading CSV file into json dict
def csvLoadingAsDict(input_path:str):
  s = csvLoadingAsString(input_path)
  jd = json.loads(s)
  return jd

def csvLoadingHead(input_path:str):
  ch = pd.read_csv(input_path)
  return ch.head()

# loading json file into string(jsonFormat)(used inside)
def jsonLoadingAsString(js_path:str):
  jf = pd.read_json(js_path)
  s = jf.to_json()
  return s

# loading json file into dict
def jsonLoadingAsDict(js_path:str):
  s = jsonLoadingAsString(js_path)
  jd = json.loads(s)
  return jd

# loading pickle file into dict
def pickleLoadingAsDict(pickle_path:str):
  with open(pickle_path,'rb') as pf:
    pd = pickle.load(pf)
  return pd



# Eventlog functions:

# save json dict as csv file
def savePredictEventlog(uuid: str, file_name: str , file: UploadFile, volume_address = ''): #Volume address logic needs to be solved later
  
  root_address = os.path.join(volume_address,predict_root,uuid)

  folder = os.path.exists(root_address)

  if not folder:
    os.makedirs(root_address)

  with open(os.path.join(root_address,file_name), 'wb') as buffer:
      shutil.copyfileobj(file, buffer)


# load EventLog address
def loadPredictEventLog(uuid: str, file_name: str, volume_address = ''):
 
  root_address = root_address = os.path.join(volume_address,predict_root,uuid,file_name)
  
  return root_address



# Pickle functions:
# save pickle dict as pickle file
def savePickle(uuid: str, file_name: str , file: UploadFile, volume_address = ''):

  root_address = os.path.join(volume_address,predict_root,uuid)

  folder = os.path.exists(root_address)

  if not folder:
    os.makedirs(root_address)

  with open(os.path.join(root_address,file_name), 'wb') as buffer:
      shutil.copyfileobj(file, buffer)


# load pickle file address by uuid and name
def loadPickle(uuid: str, file_name: str, volume_address = ''):
  
  root_address = root_address = os.path.join(volume_address,predict_root,uuid,file_name)

  return root_address



# File checking functions:
# check file existance
def fileExistanceCheck(files: List):
  result = True;

  for file in files:
    if not os.path.exists(file):
      result = False
  
  return result


# check the file in csv format
def csvCheck(file: str):

  filename,extension = os.path.splitext(file)

  if extension == '.csv':
    return True
  else:
    return False


# check the  file in pickle format
def pickleCheck(file: str):

  filename,extension = os.path.splitext(file)
  
  if extension == '.pkl' or extension == '.pickle':
    return True
  else:
    return False


# zip functions
def zipFile(uuid: str, volume_address:str = ''):

  startdir = os.path.join(volume_address,predict_root,uuid)

  if not os.path.exists(startdir):
    return False

  z = zipfile.ZipFile(startdir + '.zip', 'w', zipfile.ZIP_DEFLATED)
  
  for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
      z.write(os.path.join(dirpath, filename))
  z.close()
  
  shutil.rmtree(startdir)
  return True


# load zip address by uuid
def loadZip(uuid: str, volume_address = ''):

  zip_address = os.path.join(volume_address,predict_root,uuid)+'.zip'

  return zip_address


def removeZip(uuid: str):
  os.remove(loadZip(uuid))



# serializing functions
def baseDecode(base:str):
  return base64.decode(base)


## Docker volume test ##

# docker build -t python-project .
# docker run -it -v abc:/Predictive python-project (volume 'abc' would be created, root dir is /Predictive)
