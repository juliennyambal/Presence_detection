# Presence Detection

This repo follows the presentation made during the meetup [Johannesburg Machine Learning Meetup](https://www.meetup.com/Johannesburg-Artificial-Intelligence-Meetup/events/268234198) that was held on the 20th February 2020.

> :warning: **In this repo, I am using Windows 10**: Linux and MacOS use, check the path slashes before running the code.

# Initial Phase

Install everything python required: `pip install requirements.txt`

## Getting the data and infrastruture ready

The steps are pretty straight forward:

- [Install Docker](https://docs.docker.com/docker-for-windows/install/) and activate Docker Desktop (Admin): You will need to activate docker as admin in your system. I was using Windows 10.
- Activate RabbitMQ Docker image, by running `docker-compose up` from the terminal. If you familiar with Docker you can create your own instance from here [Bitnami Github Repo for RabbitMQ](https://github.com/bitnami/bitnami-docker-rabbitmq). The credentials are:
  - Username: **user**
  - Password: **bitnami**
  - Local server: **localhost:15672**
- Run descriptive analysis:
  - From the root folder: type in `python Dev/descriptive_analysis.py`
  - The plots should appear in the `Plots` folder

## Training the models

Origin of the dataset: [Occupancy Detection Data Set](https://archive.ics.uci.edu/ml/machine-learning-databases/00357/).

> **Commands:** 

```python Dev/occupancy_training.py```

The aim of this project is to show the ability to use a trained model and to swith whenever the model does not perform so well. The switch here does not happen automatically but the code could be modify to add to toggles for those features.

From the `Dev` folder, there is the file `occupancy_training.py` that will produce after training some models in a `.pkl` extention to be later user by the server. You would want to run the following command `python Dev/occupancy_training.py`. You should see a folder called `Models` containing all the different trained models for this task. Feel free to add other classifiers. The following table will be displayed after the training of all the models.

|                        |  Nearest Neighbors  |      Linear SVM     |    Decision Tree     |   Random Forest    |     Neural Net     |       AdaBoost      |      Naive Bayes      | Logistic Regression |
|------------------------|---------------------|---------------------|----------------------|--------------------|--------------------|---------------------|-----------------------|---------------------|
|   Balanced Accuracy    |  0.9772593030124039 |  0.9772593030124039 |  0.9772593030124039  | 0.9772593030124039 | 0.9769639692852924 |  0.9772593030124039 |   0.9769639692852924  |  0.9772593030124039 |
|           F1           |  0.9713211850274014 |  0.9713211850274014 |  0.9713211850274014  | 0.9713211850274014 | 0.9709511677910402 |  0.9713211850274014 |   0.9709511677910402  |  0.9713211850274014 |
|        Accuracy        |  0.9711069418386492 |  0.9711069418386492 |  0.9711069418386492  | 0.9711069418386492 | 0.9707317073170731 |  0.9711069418386492 |   0.9707317073170731  |  0.9711069418386492 |
|   Training time (s)    | 0.10528111457824707 | 0.08269143104553223 | 0.008838653564453125 |  1.11342191696167  | 4.297305107116699  | 0.01706552505493164 | 0.0063571929931640625 | 0.18995070457458496 |

As a plus, there is a  `Dev/TPOT.py` which is [A Python Automated Machine Learning tool that optimizes machine learning pipelines using genetic programming.](https://github.com/EpistasisLab/tpot) for some sort of auto-ml. Take a look and try to get something out of it. 

## Serving the models

- Activate the project’s server
    - `python Production/app.py`
    - open the browser and type in `localhost:5000`

Here you have to note that the current model selected in the `Random Forest`. You can change that from the deployment file `Production/app.py`.

## Experiements with one model (Random Forests)

Here you will need some sort of SQL software, I am using [MySQLWorkBench](https://dev.mysql.com/downloads/workbench/). 

Run the following commands to compare the models (**strickly in this order**):

-  `python Production/app.py` (in one terminal) This will start up the ML model,
- `python RPC/consumer.py` (in another terminal) starts the consumer (Listens on port 5000). Make sure that SQL and RabbitMQ are up and running.
- `python RPC/producer.py`(in another terminal) starts the consumer (Listens on port 5000). Make sure that SQL and RabbitMQ are up and running.
-  You should be able to track the progress of your model in your SQL software.

## Experiements with Multiple models

Here you will need some sort of SQL software, I am using [MySQLWorkBench](https://dev.mysql.com/downloads/workbench/). 

Run the following commands to compare the models (**strickly in this order**):

- `python Dev/app_kinda_ab_testing.py` (in one terminal) This will start up the ML model,
- `python RPC/consumer_kinda_ab_testing.py` (in another terminal) starts the consumer (Listens on port 5001). Make sure that SQL and RabbitMQ are up and running.
- `python RPC/producer.py`(in another terminal). Make sure that SQL and RabbitMQ are up and running.
-  You should be able to track the progress of your model in your SQL software.

To avoid this error `requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=5001): Max retries exceeded with url: /results (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000001C8A4B3C288>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))` please follow the above order.
