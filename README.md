# Presence Detection

This repo follows the presentation made during the meetup [Johannesburg Machine Learning Meetup](https://www.meetup.com/Johannesburg-Artificial-Intelligence-Meetup/events/268234198) that was held on the 20th February 2020.


# Initial Phase

## Getting the data and infrastruture ready

The steps are pretty straight forward:

- Activate Docker Desktop (Admin): You will need to activate docker as admin in your system. I was using Windows 10.
- Activate RabbitMQ Docker image. If you familiar with Docker you can create your own instance from here [Bitnami Github Repo for RabbitMQ](https://github.com/bitnami/bitnami-docker-rabbitmq). The credentials are:
  - Commmad in terminal where the `docker-compose.yml` file is, type `docker-compose up`
    - Username: **user**
    - Password: **bitnami**
    - Local server: **localhost:15672**
- Run descriptive analysis:
  - From the root folder: type in `python Dev/descriptive_analysis.py`
  - The plots should appear in the `Plots` folder

## Training the models

The aim of this project is to show the ability to use a trained model and to swith whenever the model does not perform so well. The switch here does not happen automatically but the code could be modify to add to toggles for those features.

From the `Dev` folder, there is the file `occupancy_training.py` that will produce after training some models in a `.pkl` extention to be later user by the server. You would want to run the following command `python Dev/occupancy_training.py`. You should see a folder called `Models` containing all the different trained models for this task. Feel free to add other classifiers.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |




