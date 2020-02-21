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
url = config.PREDICTION_URL_PROD


DB_NAME = config.DB_NAME
PROD_TABLE = config.DB_PROD_TABLE
TABLES = {}
TABLES['prediction'] = (
"""CREATE TABLE %s (
  `prediction_id` int(10) NOT NULL AUTO_INCREMENT,
  `Temparature` float NOT NULL,
  `Humidity` float NOT NULL,
  `Light` float,
  `CO2` float NOT NULL,
  `prediction` int,
  `emptyness_probability` float, 
  `model` varchar(255),        
  `date` datetime,
  PRIMARY KEY (`prediction_id`)
) ENGINE=InnoDB""" % PROD_TABLE)

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
    data_prediction = (data['temparature'], data['Humidity'], data['Light'], data['CO2'], int(np.clip(np.round(r['status']),0,1)),r['emptyness_proba'],r['model'],time.strftime('%Y-%m-%d %H:%M:%S'))
    insert_section = "INSERT INTO %s " % PROD_TABLE
    add_prediction = insert_section + """(Temparature, Humidity, Light, CO2, prediction,emptyness_probability,model,date) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
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