#!/usr/bin/env python
import pika
import requests
import time    
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import json

#To be modified according to the current settings
import config

QUEUE_NAME = config.RABBIT_MQ_QUEUE_NAME
RMQ_SERVER = config.RABBIT_MQ_SERVER
RMQ_PORT = config.RABBIT_MQ_PORT
USERNAME = config.RABBIT_MQ_USERNAME
PASSWORD = config.RABBIT_MQ_PASSWORD
VIRTUAL_HOST= '/'
url = config.PREDICTION_URL_DEV


"""
AdaBoostClassifier
DecisionTreeClassifier
SVC
LogisticRegression
GaussianNB
KNeighborsClassifier
MLPClassifier
RandomForestClassifier
"""


DB_NAME = config.DB_NAME
DEV_TABLE = config.DB_DEV_TABLE
TABLES = {}
TABLES['prediction'] = (
    "CREATE TABLE `predictions_ab_tests` ("
    "  `prediction_id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `Temparature` float NOT NULL,"
    "  `Humidity` float NOT NULL,"
    "  `Light` float NOT NULL,"
    "  `CO2` float NOT NULL ,"
    "  `AdaBoost_prediction` int,"
    "  `DecisionTree_prediction` int,"
    "  `SVC_prediction` int,"
    "  `LR_prediction` int,"
    "  `GNB_prediction` int,"
    "  `KNN_prediction` int,"
    "  `ANN_prediction` int,"
    "  `RF_prediction` int,"
    "  `AdaBoost_emptyness_probability` float NOT NULL,"
    "  `DecisionTree_emptyness_probability` float NOT NULL,"
    "  `SVC_emptyness_probability` float NOT NULL,"
    "  `LR_emptyness_probability` float NOT NULL,"
    "  `GNB_emptyness_probability` float NOT NULL,"
    "  `KNN_emptyness_probability` float NOT NULL," 
    "  `ANN_emptyness_probability` float NOT NULL,"
    "  `RF_emptyness_probability` float NOT NULL,"      
    "  `date` datetime,"
    "  PRIMARY KEY (`prediction_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user=config.DB_USER_NAME, password=config.DB_PASSWORD)
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


CREDENTIALS = pika.PlainCredentials(USERNAME, PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(RMQ_SERVER,
                                       RMQ_PORT,
                                       VIRTUAL_HOST,
                                       CREDENTIALS))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def predict(message):
    message = json.loads(message)
    data = message
    r = requests.post(url,json=data).json()
    data_prediction = (data['temparature'], data['Humidity'], data['Light'], data['CO2'], 
                       r['AdaBoostClassifier_prediction'],
                       r['DecisionTreeClassifier_prediction'],
                       r['SVC_prediction'],
                       r['LogisticRegression_prediction'],
                       r['GaussianNB_prediction'],
                       r['KNeighborsClassifier_prediction'],
                       r['MLPClassifier_prediction'],
                       r['RandomForestClassifier_prediction'],
                       r['AdaBoostClassifier_emptuness_proba'],
                       r['DecisionTreeClassifier_emptuness_proba'],
                       r['SVC_emptuness_proba'],
                       r['LogisticRegression_emptuness_proba'],
                       r['GaussianNB_emptuness_proba'],
                       r['KNeighborsClassifier_emptuness_proba'],
                       r['MLPClassifier_emptuness_proba'],
                       r['RandomForestClassifier_emptuness_proba'],
                       time.strftime('%Y-%m-%d %H:%M:%S'))
    print(data_prediction)
    insert_section = "INSERT INTO %s " % DEV_TABLE
    add_prediction = (insert_section+
    "(Temparature,Humidity,Light,CO2 ,AdaBoost_prediction,DecisionTree_prediction,SVC_prediction,LR_prediction,GNB_prediction,KNN_prediction,ANN_prediction,RF_prediction,AdaBoost_emptyness_probability,DecisionTree_emptyness_probability,SVC_emptyness_probability,LR_emptyness_probability,GNB_emptyness_probability,KNN_emptyness_probability,ANN_emptyness_probability,RF_emptyness_probability,date) "
    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    cursor.execute(add_prediction, data_prediction)
    cnx.commit()
    return data_prediction


def on_request(ch, method, props, body):
    print(" [.] Received (%s)" % body.decode('utf-8'))
    response = predict(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()