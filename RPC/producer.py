#!/usr/bin/env python
import pika
import uuid
from time import sleep

import config

import numpy as np
import random
import mysql.connector
from mysql.connector import errorcode
import json

QUEUE_NAME = config.RABBIT_MQ_QUEUE_NAME
RMQ_SERVER = config.RABBIT_MQ_SERVER
RMQ_PORT = config.RABBIT_MQ_PORT
USERNAME = config.RABBIT_MQ_USERNAME
PASSWORD = config.RABBIT_MQ_PASSWORD
VIRTUAL_HOST= config.RABBIT_MQ_VIRTUAL_HOST
EXCHANGE = config.RABBIT_MQ_EXCHANGE
ROUTING_KEY = config.RABBIT_MQ_ROUTING_KEY

class RpcClient(object):
    
    def __init__(self):
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RMQ_SERVER,
                                       port=RMQ_PORT,
                                       credentials=credentials))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=QUEUE_NAME,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)
        while self.response is None:
           self.connection.process_data_events()
        return self.response


client = RpcClient()

for i in range(10000):
    temp = random.uniform(19, 24)
    hum = random.uniform(18, 39)
    light = random.uniform(0, 1600)
    co2 = random.uniform(420, 2030)

    data = json.dumps({'temparature':temp, 'Humidity':hum, 'Light':light, 'CO2':co2})
    print("Sent: ", data)
    print(" [.] Got %r" % client.call(data).decode('utf-8'))
    sleep(1)