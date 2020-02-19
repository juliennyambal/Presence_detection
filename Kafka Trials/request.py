from __future__ import print_function
import requests
import time    
import random
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import uuid
from time import sleep
from kafka import KafkaProducer, KafkaConsumer
import json

url = 'http://localhost:5000/results'

def start_producing(message):
    producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)
    message_id = str(uuid.uuid4())
    message = {'request_id': message_id, 'data': json.loads(message)}
    producer.send('occupancy', json.dumps(message).encode('utf-8'))
    producer.flush()
    print("\033[1;31;40m -- PRODUCER: Sent message with id {}".format(message_id))

for i in range(10000):
    temp = random.uniform(19, 24)
    hum = random.uniform(18, 39)
    light = random.uniform(0, 1600)
    co2 = random.uniform(420, 2030)

    #r = requests.post(url,json={'temparature':temp, 'Humidity':hum, 'Light':light, 'CO2':co2 }).json()
    #data_prediction = (temp, hum, light, co2, int(np.clip(np.round(r['status']),0,1)),time.strftime('%Y-%m-%d %H:%M:%S'))
    data = json.dumps({'temparature':temp, 'Humidity':hum, 'Light':light, 'CO2':co2})
    start_producing(data)
    print(data)
    sleep(5)