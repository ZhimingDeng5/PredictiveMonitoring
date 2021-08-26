# Predictive Monitoring

Apromore is a company providing leading open-source process mining software to management and process optimization consultancies worldwide, see more details at https://apromore.org/. Apromore already has a solution providing predictive monitoring capabilities. This project will provide a robust, scalable and performative solution for the predictive monitoring plugin. And this will be capable of handling a loads of up to a hundred million event logs and integrated with the open-source ApromoreCore project.

## Objectives
The goal of the project is to create two stand-alone (i.e. independent from the already existing Apromore platform) modules, one responsible for training predictors, and the other for delivering predictions. The modules are meant to be production-grade, scalable, fault-tolerant, performative and operating in an asynchronous manner. The focus of the project is on creating a robust back-end around the machine learning library responsible for creating predictors and predictions, provided by Apromore. The front-end needs to be functional, but there is no need to commit too many resources on its development, as it will eventually be abandoned in lieu of a front-end designed by the Apromore team once our project gets integrated with the main platform.

The project will only create predictions based on batch event log uploads (as opposed to consuming live event feeds).

## Sprint 1 Deployment

Ensure Docker and Docker Compose have been setup on your local machine. After cloning the repository, use Docker Compose:
```
$ cd PredictiveMonitoring/src
$ docker-compose up --build --scale predictive-worker=3
```