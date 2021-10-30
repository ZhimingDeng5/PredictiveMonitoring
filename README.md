# Predictive Monitoring

Apromore is a company providing leading open-source process mining software to management and process optimization consultancies worldwide, see more details at https://apromore.org/. Apromore already has a solution providing predictive monitoring capabilities. This project will provide a robust, scalable and performative solution for the predictive monitoring plugin. And this will be capable of handling a loads of up to a hundred million event logs and integrated with the open-source ApromoreCore project.

## Objectives
The goal of the project is to create two stand-alone (i.e. independent from the already existing Apromore platform) modules, one responsible for training predictors, and the other for delivering predictions. The modules are meant to be production-grade, scalable, fault-tolerant, performative and operating in an asynchronous manner. The focus of the project is on creating a robust back-end around the machine learning library responsible for creating predictors and predictions, provided by Apromore. The front-end needs to be functional, but there is no need to commit too many resources on its development, as it will eventually be abandoned in lieu of a front-end designed by the Apromore team once our project gets integrated with the main platform.

The project will only create predictions based on batch event log uploads (as opposed to consuming live event feeds).

## Single node deployment

Ensure Docker and Docker Compose have been setup on your local machine. After cloning the repository, use Docker Compose:

Navigate to the src folder
```
$ cd PredictiveMonitoring/src
```
Start the service with the following command, setting the desired number of worker nodes for the training and prediction modules
```
$ docker-compose up --build --scale worker-prediction=3 --scale worker-training=3
```

## Swarm deployment

Swarm deployment in its current version uses vieux/sshfs as the volume driver. Start by installing the plugin on the manager node of the swarm.
```
$ docker plugin install vieux/sshfs
```
Then configure the docker-compose-swarm.yml file (inside the /src folder) to connect to a server on which you're intending to host the volume by filling in the **username**, **host** and **path#** fields. Make sure that the paths exist on the host before deploying the stack, as the driver will not create them on its own. Use different paths for each volume to file name clashes.
```
    ssh_training:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: <username>@<host>:<path1>
            password: <password>
            allow_other: ""
    ssh_predict:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: "<username>@<host>:<path2>"
            password: <password>
            allow_other: ""
    ssh_task:
        driver: vieux/sshfs:latest
        driver_opts:
            sshcmd: "<username>@<host>:<path3>"
            password: <password>
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
