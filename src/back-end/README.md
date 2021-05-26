# TestApp

This project was generated with [Fast Api](https://fastapi.tiangolo.com) version 0.65.1.

## Install the Environment and Run the project

- Run `pip install -r requirements.txt` to install the environment.
- Run `python run.py` to start the back end.

## API Tests

### Swagger UI

The server will run at http://127.0.0.1:8000

The interactive document address is http://127.0.0.1:8000/docs .

All API can be tested in this open API page.

### Predict Module

#### Test the module

```
Get: http://localhost:8000/predictive_monitor
Params: {},
return: {'message': 'This is predictive monitor module'}
```

#### Test this create_monitor function

```
post: http://localhost:8000/predictive_monitor/create_monitor
Params: {
    'monitor_name': str, 
    'pickle_files': List[UploadFile] = File(...),
    'schema_file': UploadFile = File(...)
    }
return:  {
    'monitor_name': monitor_name, 
    'pickle_files': [file.filename for file in pickle_files],
    'schema_file': schema_file.filename
    }
```

### Traning Module

#### Test the module

```
get: http://localhost:8000/training/
Params: {}
return: {'message': 'This is training module'}
```

#### Test this generate_predictor function

```
post: http://localhost:8000/training/generate_predictor
Params: {
    'predictor_type': PredictorType, 
    'predictor_name': str, 
    'event_log_file': UploadFile = File(...),
    'schema_file': UploadFile = File(...)
    }
return:  {
    "predictor_type": predictor_type, 
    'predictor_name': predictor_name,
    'event_log_file': event_log_file.filename, 
    'schema_file': schema_file.filename
    }
```
