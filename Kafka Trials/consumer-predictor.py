from __future__ import print_function
import requests
import time    
import random
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import uuid
from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_HOST = 'localhost:9092'
DB_NAME = 'incubator_ds'
TABLES = {}
TABLES['prediction'] = (
    "CREATE TABLE `predictions_lr` ("
    "  `prediction_id` int(10) NOT NULL AUTO_INCREMENT,"
    "  `Temparature` float NOT NULL,"
    "  `Humidity` float NOT NULL,"
    "  `Light` float,"
    "  `CO2` float NOT NULL,"
    "  `prediction` int,"
    "  `date` datetime,"
    "  PRIMARY KEY (`prediction_id`)"
    ") ENGINE=InnoDB")

cnx = mysql.connector.connect(user='root', password='@Entelect')
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

url = 'http://localhost:5000/results'



def start_consuming():
    consumer = KafkaConsumer('occupancy', bootstrap_servers=KAFKA_HOST)
    for msg in consumer:
        message = json.loads(msg.value)
        if 'data' in message:
            request_id = message['request_id']
            data = message['data']
            r = requests.post(url,json=data).json()
            print("\033[1;32;40m ** CONSUMER: Received prediction {} for request id {}".format(int(np.clip(np.round(r['status']),0,1)), request_id))
            data_prediction = (data['temparature'], data['Humidity'], data['Light'], data['CO2'], int(np.clip(np.round(r['status']),0,1)),time.strftime('%Y-%m-%d %H:%M:%S'))
            add_prediction = ("INSERT INTO predictions_lr "
            "(Temparature, Humidity, Light, CO2, prediction,date) "
            "VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(add_prediction, data_prediction)
            cnx.commit()
start_consuming()

cursor.close()
cnx.close()
