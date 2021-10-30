# Predictive Monitoring

Apromore is a company providing leading open-source process mining software to management and process optimization consultancies worldwide, see more details at https://apromore.org/. Apromore already has a solution providing predictive monitoring capabilities. This project will provide a robust, scalable and performative solution for the predictive monitoring plugin. And this will be capable of handling a loads of up to a hundred million event logs and integrated with the open-source ApromoreCore project.

# Objectives
The goal of the project is to create two stand-alone (i.e. independent from the already existing Apromore platform) modules, one responsible for training predictors, and the other for delivering predictions. The modules are meant to be production-grade, scalable, fault-tolerant, performative and operating in an asynchronous manner. The focus of the project is on creating a robust back-end around the machine learning library responsible for creating predictors and predictions, provided by Apromore. The front-end needs to be functional, but there is no need to commit too many resources on its development, as it will eventually be abandoned in lieu of a front-end designed by the Apromore team once our project gets integrated with the main platform.

The project will only create predictions based on batch event log uploads (as opposed to consuming live event feeds).

# Single node deployment

Ensure Docker and Docker Compose have been setup on your local machine. After cloning the repository, use Docker Compose:

Navigate to the src folder
```
$ cd PredictiveMonitoring/src
```
Start the service with the following command, setting the desired number of worker nodes for the training and prediction modules
```
$ docker-compose up --build --scale worker-prediction=3 --scale worker-training=3
```

# Swarm deployment

Swarm deployment in its current version uses vieux/sshfs as the volume driver. Start by installing the plugin on the manager node of the swarm.
```
$ docker plugin install vieux/sshfs
```
Then configure the docker-compose-swarm.yml file (inside the /src folder) to connect to a server on which you're intending to host the volume by filling in the **username**, **host** and **path#** fields. Make sure that the paths exist on the host before deploying the stack, as the driver will not create them on its own. Use different paths for each volume to file name clashes.
```
    ssh_training:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: "<username>@<host>:<path1>"
            password: "<password>"
            allow_other: ""
    ssh_predict:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: "<username>@<host>:<path2>"
            password: "<password>"
            allow_other: ""
    ssh_task:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: "<username>@<host>:<path3>"
            password: "<password>"
            allow_other: ""
```

Now we should be ready to deploy the stack. Navigate to the src folder.
```
$ cd PredictiveMonitoring/src
```
On the master node of your swarm log into the predictivemonitor repo with **$ docker login**, then run the following command
```
$ docker stack deploy --with-registry-auth -c docker-compose-swarm.yml
```

# Data samples
Sample data to test the application is available in the /DataSamples folder

# APIs
## /prediction module
### /create-dashboard
Endpoint used to start a dashboard creation task.
#### Parameters:
No parameters
#### Request body:
- event_log: file in either .csv or .parquet format
- predictors: array of pickle files containing trained ML models
- schema: a json file describing the schema of the event log and predictors
#### Return value:
- {task_id: <ID of the created task>}.
### /cancel/{taskID}
Endpoint used to cancel a dashboard creation task.
#### Parameters:
- taskID: UUID of the task to be cancelled
#### Return value:
- {taskID: <ID of the cancelled task>, status: CANCELLED}
- ### /tasks
Endpoint used to get the status of all tasks in the system.
#### Parameters:
No parameters
#### Return value:
- {tasks: [{taskID: UUID, status: QUEUED/PROCESSING/COMPLETED/ERROR, error_msg: ""}...]}
### / task/{taskIDs}
Endpoint used to get status of selected tasks.
#### Parameters:
- taskIDs: & separated string of UUID
#### Return value:
- {tasks: [{taskID: UUID, status: QUEUED/PROCESSING/COMPLETED/ERROR, error_msg: ""}...]}
- ### /dashboard/{taskID}
Endpoint used to retrieve a created dashboard.
#### Parameters:
- taskID: UUID of the task whose dashboard we want to retrieve
#### Return value:
- csv formatted dashboard containing predictions for the corresponding event logs
## /training module
### /create-predictor
Endpoint used to start a predictor training task.
#### Parameters:
No parameters
#### Request body:
- event_log: file in either .csv or .parquet format
- config: a json file containing the configuration of the training task
- schema: a json file describing the schema of the event log
#### Return value:
- {task_id: <ID of the created task>}
### /cancel/{taskID}
Endpoint used to cancel a predictor training task.
#### Parameters:
- taskID: UUID of the task to be cancelled
#### Return value:
- {taskID: <ID of the cancelled task>, status: CANCELLED}
### /tasks
Endpoint used to get the status of all tasks in the system.
#### Parameters:
No parameters.
#### Return value:
- {tasks: [{taskID: UUID, status: QUEUED/PROCESSING/COMPLETED/ERROR, error_msg: ""}...]}
### / task/{taskIDs}
Endpoint used to get status of selected tasks.
#### Parameters:
- taskIDs: & separated string of UUID
#### Return value:
- {tasks: [{taskID: UUID, status: QUEUED/PROCESSING/COMPLETED/ERROR, error_msg: ""}...]}
### /predictor/{taskID}
Endpoint used to retrieve a trained predictor.
#### Parameters:
- taskID: UUID of the task whose predictor we want to retrieve.
#### Return value:
- zip file contained the predictor in .pkl format and a number of .csv files detailing the predictor performance.

# Live access
You can access a single node deployment of the app at https://apromore-predict.cloud.ut.ee/
