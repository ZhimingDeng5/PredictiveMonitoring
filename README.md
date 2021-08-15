# Predictive Monitoring

Apromore is a company providing leading open-source process mining software to management and process optimization consultancies worldwide, see more details at https://apromore.org/. Apromore already has a solution providing predictive monitoring capabilities. This project will provide a robust, scalable and performative solution for the predictive monitoring plugin. And this will be capable of handling a loads of up to a hundred million event logs and integrated with the open-source ApromoreCore project.

## Objectives
The goal of the project is to create two stand-alone (i.e. independent from the already existing Apromore platform) modules, one responsible for training predictors, and the other for delivering predictions. The modules are meant to be production-grade, scalable, fault-tolerant, performative and operating in an asynchronous manner. The focus of the project is on creating a robust back-end around the machine learning library responsible for creating predictors and predictions, provided by Apromore. The front-end needs to be functional, but there is no need to commit too many resources on its development, as it will eventually be abandoned in lieu of a front-end designed by the Apromore team once our project gets integrated with the main platform.

The project will only create predictions based on batch event log uploads (as opposed to consuming live event feeds).

## Sprint 1 Deployment

On the server (i.e., apromore-predict.cloud.ut.ee) use Docker Compose to deploy the services:
```
$ cd deployment/PredictiveMonitoring/src
$ docker-compose down
$ docker-compose up --build --scale predictive-worker=3
```

The front-end is deployed at https://apromore-predict.cloud.ut.ee/test-app, and the backend servieces are deployed at https://apromore-predict.cloud.ut.ee/backend.

Test create_dashbord: 
```
curl -X 'POST' 'https://apromore-predict.cloud.ut.ee/backend/create-dashboard?name=<NAME>' -H 'accep-F 'event_log=@<LOG_FILE>;type=text/plain'ta' -F 'monitor=@<MONITOR_FILE>;type=text/plain'
```
Please replace `<NAME>` with a task name (e.g., test),  and replace `<LOG_FILE>` and `<MONITOR_FILE>` with two .txt files.

Then, tasks can be viewed at: https://apromore-predict.cloud.ut.ee/backend/tasks

### For Local Test
replace `http(s)://apromore-predict.cloud.ut.ee` with `localhost` in the `caddy/Caddyfile`.
Then the services will be deployed on localhost via following commands:
```
$ docker-compose down
$ docker-compose up --build --scale predictive-worker=3
```
